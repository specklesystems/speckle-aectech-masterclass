from array import array
from hashlib import new
from logging import NullHandler
from types import AsyncGeneratorType
from typing import Any, List
from math import floor

from specklepy.api import operations
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from specklepy.api.models import Branch
from specklepy.api.resources import stream
from specklepy.transports.server import ServerTransport
from specklepy.objects.geometry import GEOMETRY, Box, Brep, Point, Mesh, Line
from specklepy.objects import Base
from specklepy.objects.other import RenderMaterial

import os

URL = 'https://speckle.xyz/streams/'
HOST = "latest.speckle.dev"
STREAM_ID = "8325294b8f"
COMMIT_ID = "c207299871"  # current commit
PREV_COMMIT_ID = "b9f376d75d"  # previous commit
DIFF_BRANCH = "diff"
COLORS = [-6426, -13108, -19790, -26215, -
          32640, -39322, -45747, -52429, -59111, -65536]
WHITE = -1


def get_authenticated_client(token: str) -> SpeckleClient:
    client = SpeckleClient(host=HOST)
    client.authenticate(token=token)
    return client


def receive_data(
    client: SpeckleClient, stream_id: str, commit_id: str
) -> Any:
    transport = ServerTransport(client, stream_id)

    commit = client.commit.get(stream_id, commit_id)
    res = operations.receive(commit.referencedObject, transport)

    # if grasshopper, will be nested under data: res["data"]
    # if rhino/autocad/revit, will be sent with layers or categories

    return res

def get_all_meshes(child: Base):
    meshes = []

    names = child.get_dynamic_member_names()
    for name in names:
        prop = child[name]
        if isinstance(prop, Base):
            if isinstance(prop, Brep):
                if not hasattr(prop, "displayMesh"):
                    break
                meshes.append((prop.displayMesh, prop.id, prop.applicationId, prop))
            elif isinstance(prop, Mesh):
                meshes.append((prop, prop.id, prop.applicationId))
        elif isinstance(prop, list):  
            for p in prop:
                if isinstance(p, Brep):
                    if not hasattr(p, "displayMesh"):
                        break
                    meshes.append((p.displayMesh, p.id, p.applicationId, p))
                elif isinstance(p, Mesh):
                    meshes.append((p, p.id, p.applicationId))
    return meshes


def get_all_points(meshes: List[Mesh]):
    points = []
    for mesh in meshes:
        for i in range(2, len(mesh.vertices), 3):
            point = Point()
            point.x = mesh.vertices[i-2]
            point.y = mesh.vertices[i-1]
            point.z = mesh.vertices[i]
            points.append(point)
    return points


def find_point(current: Point, points: List[Point]):
    for point in points:
        if (point.x == current.x and point.y == current.y and point.z == current.z):
            return True
    return False


def find_closest_point(current: Point, points: List[Point]):
    smallest_distance = None
    for point in points:
        d = ((current.x - point.x)**2 + (current.y - point.y)
             ** 2 + (current.z - point.z)**2)**0.5
        if smallest_distance is not None:
            if d > smallest_distance:
                continue
        smallest_distance = d
    return smallest_distance

def check_existing_commits(
    client: SpeckleClient, stream_id: str, commit_current: str, commit_previous: str
) -> Any:
    transport = ServerTransport(client, stream_id)

    branch_commits: Branch = client.branch.get(stream_id, DIFF_BRANCH, 50)
    
    for commit in branch_commits.commits.items:
        if commit.message == f"{commit_current}-{commit_previous}":
            return commit.id

    return None


def compare_meshes(stream_id: str, commit_current: str, commit_previous: str):
    client = get_authenticated_client()

    # see if existing diff commit already exists
    # query for latest x commits in diff branch
    # read commit message & parse
    # return url if found
    existing_commit = check_existing_commits(client, stream_id, commit_current, commit_previous)
    if existing_commit is not None:
        url = URL + stream_id + '/commits/' + existing_commit 
        return url

    # get meshes from commits
    previous_commit = receive_data(client, stream_id, commit_previous)
    previous_meshes = get_all_meshes(previous_commit)
    current_commit = receive_data(client, stream_id, commit_current)
    current_meshes = get_all_meshes(current_commit)

    # pre process meshes in the current commit to check for same object ID (this means obj hasn't changed) - skip these
    # if object id has changed, check for application id - if these are the same, compare these objects directly
    matched_current_indices = []
    matched_previous_indices = []
    paired_current_indices = []
    paired_previous_indices =[]
    for i in range(0, len(current_meshes), 1):
        for j in range(0, len(previous_meshes), 1):
            if current_meshes[i][1] == previous_meshes[j][1]:
                matched_current_indices.append(i)
                matched_previous_indices.append(j)
                break
            elif current_meshes[i][2] == previous_meshes[j][2]:
                paired_current_indices.append(i)
                paired_previous_indices.append(j)
                break

    # remove matched previous meshes and matched pairs and get list of all mesh points from processed list
    # this will be used as reference for all meshes that have changed and don't have a specific match to compare to
    previous_meshes_ref_pool = []
    for i in range(0, len(previous_meshes), 1):
        if matched_previous_indices.__contains__(i) or paired_previous_indices.__contains__(i):
            continue
        previous_meshes_ref_pool.append(previous_meshes[i][0])
    ref_pool = get_all_points(previous_meshes_ref_pool)

    # create a ghosted render material
    ghosted = RenderMaterial()
    ghosted.diffuse = WHITE
    ghosted.opacity = 0.1

    # for each mesh in the current commit, compare mesh vertices with ref pool or matched pair to determine scale of change
    diff_meshes = []
    same_meshes = []
    ref_meshes = []
    diff_mesh_pairs = []
    diff_mesh_ref_indices = [] # the corresponding ref pair mesh to diff mesh pairs
    for i in range(0, len(current_meshes), 1):
        mesh = current_meshes[i][0]

        # send matched current meshes with rendermaterial semi-transparent (ghosted)
        if matched_current_indices.__contains__(i):
            mesh.renderMaterial = ghosted
            same_meshes.append(mesh)
            continue

        diff_mesh = mesh
        vertices = get_all_points([mesh])
        diff_mesh_colors = [WHITE] * (len(vertices))
        diff_values = []

        # check for pairing
        paired_mesh_points = []
        paired_ref_mesh_index = None
        is_paired = False
        if paired_current_indices.__contains__(i):
            paired_ref_mesh_index = paired_previous_indices[paired_current_indices.index(i)]
            paired_mesh_points = get_all_points([previous_meshes[paired_ref_mesh_index][0]])
            is_paired = True

        for vertex in vertices:
            if is_paired:
                 diff_values.append(find_closest_point(vertex, paired_mesh_points))
            else:
                diff_values.append(find_closest_point(vertex, ref_pool))
        
        # determine color value for vertex by remapping domain
        changed = False
        bin_size = max(diff_values) / len(COLORS)
        for i in range(0, len(vertices), 1):
            if diff_values[i] == 0:
                continue
            else:
                index = floor(diff_values[i] / bin_size)
                if index == len(COLORS):
                    index -= 1
                diff_mesh_colors[i] = COLORS[index]
                changed = True
        
        
        if not changed: # if hasn't changed, append to same list
            mesh.renderMaterial = ghosted
            if is_paired:
                matched_previous_indices.append(paired_ref_mesh_index)
            same_meshes.append(mesh)

        else: # set colors and add mesh to diff list or paired diff list
            diff_mesh.colors = diff_mesh_colors
            if is_paired:
                diff_mesh_pairs.append(diff_mesh)
                diff_mesh_ref_indices.append(paired_ref_mesh_index)
            else:
                diff_meshes.append(diff_mesh)

    # process reference meshes
    diff_mesh_refs = []
    for j in range(0, len(previous_meshes)):
        if matched_previous_indices.__contains__(j) or diff_mesh_ref_indices.__contains__(j): # skip matched reference meshes and paired refs
            continue
        mesh = previous_meshes[j][0]
        mesh.renderMaterial = ghosted
        ref_meshes.append(mesh)
    for diff_mesh_ref_index in diff_mesh_ref_indices:
        mesh = previous_meshes[diff_mesh_ref_index]
        if len(mesh) > 3:
            diff_mesh_refs.append(mesh[3])
        else:
            diff_mesh_refs.append(mesh[0])
    
    # get units from first mesh in current commit
    units = current_meshes[0][0].units

    # create a new commit with the diff meshes
    return send_diff_data(stream_id, commit_current, commit_previous, units, diff_meshes, diff_mesh_pairs, diff_mesh_refs, same_meshes, ref_meshes)


def send_diff_data(stream_id: str, commit_current: str, commit_previous: str, units: str, changed: List[Mesh], changed_pairs: List[Mesh], ref_pairs: List[Base], unchanged: List[Mesh], ref: List[Mesh]):
    client = get_authenticated_client()

    # create a branch if necessary
    branches = client.branch.list(stream_id)
    has_res_branch = any(b.name == DIFF_BRANCH for b in branches)
    if not has_res_branch:
        client.branch.create(
            stream_id, name=DIFF_BRANCH, description="all your stream diff results"
        )

    # create a commit with message "current_commit_id - previous_commit_id"
    base = Base()
    base.units = units
    base["changed"] = changed

    for i in range(0, len(changed_pairs), 1):
        layer = f"changed::{i}"
        base[f"{layer}::changed"] = [changed_pairs[i]]
        base[f"{layer}::ref"] = [ref_pairs[i]]
    base["same"] = unchanged
    base["ref"] = ref

    transport = ServerTransport(client=client, stream_id=stream_id)

    hash = operations.send(base=base, transports=[transport])

    commit_id = client.commit.create(
        stream_id,
        hash,  # object id
        DIFF_BRANCH,
        message=commit_current + "-" + commit_previous
    )

    return URL + stream_id + '/commits/' + commit_id 

# uncomment for debug
# compare_meshes(STREAM_ID, COMMIT_ID, PREV_COMMIT_ID)

