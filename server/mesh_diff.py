from array import array
from hashlib import new
from logging import NullHandler
from types import AsyncGeneratorType
from typing import Any, List
from math import floor

from specklepy.api import operations
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from specklepy.api.resources import stream
from specklepy.transports.server import ServerTransport
from specklepy.objects.geometry import GEOMETRY, Box, Point, Mesh, Line
from specklepy.objects import Base
from specklepy.objects.other import RenderMaterial

import os


HOST = "speckle.xyz"
#STREAM_ID = "8325294b8f"
#COMMIT_ID = "d930269725"  # current commit
#PREV_COMMIT_ID = "e9d8f67969"  # previous commit
DIFF_BRANCH = "diff"
COLORS = [-6426, -13108, -19790, -26215, -32640, -39322, -45747, -52429, -59111, -65536]
WHITE = -1

def get_authenticated_client() -> SpeckleClient:
    client = SpeckleClient(host=HOST)
    account = get_default_account()
    client.authenticate(token=account.token)

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

def get_all_meshes(child:Base):
    meshes = []

    names = child.get_dynamic_member_names()
    for name in names:
        prop = child[name]
        if isinstance(prop, Base):
            if isinstance(prop, Mesh):
                meshes.append((prop, prop.id))
            else:
                if not hasattr(prop, "displayMesh"):
                    break
                meshes.append((prop.displayMesh, prop.id))
        elif isinstance(prop, list):  
            for p in prop:
                if isinstance(p, Mesh):
                    meshes.append((p, p.id))
                else:
                    if not hasattr(p, "displayMesh"):
                        break
                    meshes.append((p.displayMesh, p.id))
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
        d = ((current.x - point.x)**2 + (current.y - point.y)**2 + (current.z - point.z)**2)**0.5
        if smallest_distance is not None:
            if d > smallest_distance:
                continue
        smallest_distance = d
    return smallest_distance


def compare_meshes(stream_id: str, commit_current: str, commit_previous: str):
    client = get_authenticated_client()

    # see if existing diff commit already exists
    # query for latest x commits in diff branch
    # read commit message & parse 
    # return url if found

    # get meshes from commits
    previous_commit = receive_data(client, stream_id, commit_previous)
    previous_meshes = get_all_meshes(previous_commit)
    current_commit = receive_data(client, stream_id, commit_current)
    current_meshes = get_all_meshes(current_commit)

    # pre process meshes in the current commit to check for same object ID (this means obj hasn't changed) - skip these
    matched_current_indices = []
    matched_previous_indices = []
    for i in range(0, len(current_meshes), 1):
        for j in range(0, len(previous_meshes), 1):
            if current_meshes[i][1] == previous_meshes[j][1]:
                matched_current_indices.append(i)
                matched_previous_indices.append(j)
                break

    # remove matched previous meshes and get list of all mesh points from processed list
    previous_meshes_ref = []
    for i in range(0, len(previous_meshes), 1):
        if matched_previous_indices.__contains__(i):
            continue
        previous_meshes_ref.append(previous_meshes[i][0])
    previous_points = get_all_points(previous_meshes_ref)

    # create a ghosted render material
    ghosted = RenderMaterial()
    ghosted.diffuse = WHITE
    ghosted.opacity = 0.1

    # for each mesh in the current commit, compare face vertices with all previous points to determine edges that have changed
    diff_meshes = []
    match_meshes = []
    prev_meshes = []
    for i in range(0, len(current_meshes), 1):
        mesh = current_meshes[i][0]

        # send matched current meshes with rendermaterial semi-transparent (ghosted)
        if matched_current_indices.__contains__(i):
            mesh.renderMaterial = ghosted
            match_meshes.append(mesh)
            continue

        diff_mesh = mesh
        vertices = get_all_points([mesh])
        diff_mesh_colors = [WHITE] * (len(vertices))
        diff_values = []
        for vertex in vertices:
            diff_values.append(find_closest_point(vertex, previous_points))
        
        # determine color value for vertex by remapping domain
        bin_size = max(diff_values) / len(COLORS)
        for i in range(0, len(vertices), 1):
            if diff_values[i] == 0:
                continue
            else:
                index = floor(diff_values[i] / bin_size)
                if index == len(COLORS):
                    index -= 1
                diff_mesh_colors[i] = COLORS[index]

        # set colors and add mesh to list
        diff_mesh.colors = diff_mesh_colors
        diff_meshes.append(diff_mesh)

    # send previous commit meshes as well, with rendermaterial semi-transparent (ghosted)
    for previous_mesh in previous_meshes:
        mesh = previous_mesh[0]
        mesh.renderMaterial = ghosted
        prev_meshes.append(mesh)

    # create a new commit with the diff meshes and changed edges
    return send_diff_data(stream_id, commit_current, commit_previous, diff_meshes, match_meshes, prev_meshes)


def send_diff_data(stream_id: str, commit_current: str, commit_previous: str, meshes: List[Mesh], unchanged: List[Mesh], prev: List[Mesh]):
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
    base["changed"] = meshes
    base["same"] = unchanged
    base["ref"] = prev

    transport = ServerTransport(client=client, stream_id=stream_id)

    hash = operations.send(base=base, transports=[transport])

    commit_id = client.commit.create(
        stream_id,
        hash, # object id
        DIFF_BRANCH,
        message= commit_current + "-" + commit_previous
    )

    return 'https://speckle.xyz/streams/' + stream_id + '/commits/' + commit_id 

    

