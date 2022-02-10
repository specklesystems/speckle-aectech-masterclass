"""SpeckleMeshDiff for AEC Tech Masterclass"""

from typing import List
import math
from specklepy.api import operations
from specklepy.api.client import SpeckleClient
from specklepy.api.models import Branch
from specklepy.transports.server import ServerTransport
from specklepy.objects.geometry import Brep, Point, Mesh
from specklepy.objects import Base
from specklepy.objects.other import RenderMaterial

COLORS = [-6426, -13108, -19790, -26215, -32640, -39322, -45747, -52429, -59111, -65536]
WHITE = -1


class SpeckleMeshDiff:
    """Class to handle diffing between commits in a stream."""

    client: SpeckleClient = None
    host: str = None
    diff_branch: str = None

    commit_prev: str = None
    commit_current: str = None
    stream_id: str = None

    def __init__(self, token: str, host: str = "https://speckle.xyz", diff_branch: str = "diff"):
        self.host = host
        self.diff_branch = diff_branch
        self.client = SpeckleClient(host=self.host)
        self.client.authenticate(token=token)

    def process_diff(self, stream_id: str, commit_current: str, commit_previous: str):
        """
        Process a diff operation between the specified
        'current' commit and the 'previous' one.
        """
        # Set the global variables
        self.stream_id = stream_id
        self.commit_current = commit_current
        self.commit_prev = commit_previous

        print("Did not find existing diff, fetching commits now....")
        # get meshes from commits
        previous_commit = self.receive_data(
            self.client, self.stream_id, self.commit_prev)
        previous_meshes = self.get_all_meshes(previous_commit)

        current_commit = self.receive_data(
            self.client, self.stream_id, self.commit_current)
        current_meshes = self.get_all_meshes(current_commit)

        print("Comparing meshes...")
        diff_base = self.compare_meshes(current_meshes, previous_meshes)

        print("Diffing was successfull, sending to Speckle")
        diff_commit_id = self.send_data(
            self.client,
            self.stream_id,
            self.diff_branch,
            diff_base,
            self.commit_current + "-" + self.commit_prev)

        print("Successfully sent data to Speckle")
        return self.client.commit.get(self.stream_id, diff_commit_id)

    def check_existing_commits(self) -> bool or None:
        """Checks if a specific diff commit already exists in the diff_branch"""
        branch_commits: Branch = self.client.branch.get(
            self.stream_id, self.diff_branch, 50)
        if(branch_commits is None):
            return None
        for commit in branch_commits.commits.items:
            if commit.message == f"{self.commit_current}-{self.commit_prev}":
                return commit

        return None

    def compare_meshes(self, current_meshes: List[Mesh], previous_meshes: List[Mesh]) -> Base:
        """
        Compares the meshes from the first commit against the second, and sends the result to the `diff` branch.
        It returns the commit url of the diff.
        """

        # pre process meshes in the current commit to check for same object ID (this means obj hasn't changed) - skip these
        # if object id has changed, check for application id - if these are the same, compare these objects directly
        matched_current_indices = []
        matched_previous_indices = []
        paired_current_indices = []
        paired_previous_indices = []
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
        ref_pool = self.get_all_points(previous_meshes_ref_pool)

        # create a ghosted render material
        ghosted = RenderMaterial()
        ghosted.diffuse = WHITE
        ghosted.opacity = 0.1

        # for each mesh in the current commit, compare mesh vertices with ref pool or matched pair to determine scale of change
        diff_meshes = []
        same_meshes = []
        ref_meshes = []
        diff_mesh_pairs = []
        diff_mesh_ref_indices = []  # the corresponding ref pair mesh to diff mesh pairs
        for i in range(0, len(current_meshes), 1):
            mesh = current_meshes[i][0]

            # send matched current meshes with rendermaterial semi-transparent (ghosted)
            if matched_current_indices.__contains__(i):
                mesh.renderMaterial = ghosted
                same_meshes.append(mesh)
                continue

            diff_mesh = mesh
            vertices = self.get_all_points([mesh])
            diff_mesh_colors = [WHITE] * (len(vertices))
            diff_values = []

            # check for pairing
            paired_mesh_points = []
            paired_ref_mesh_index = None
            is_paired = False
            if paired_current_indices.__contains__(i):
                paired_ref_mesh_index = paired_previous_indices[paired_current_indices.index(
                    i)]
                paired_mesh_points = self.get_all_points(
                    [previous_meshes[paired_ref_mesh_index][0]])
                is_paired = True

            for vertex in vertices:
                if is_paired:
                    diff_values.append(self.find_closest_point(
                        vertex, paired_mesh_points))
                else:
                    diff_values.append(
                        self.find_closest_point(vertex, ref_pool))

            # determine color value for vertex by remapping domain
            changed = False
            bin_size = max(diff_values) / len(COLORS)
            for i in range(0, len(vertices), 1):
                if diff_values[i] == 0:
                    continue
                else:
                    index = math.floor(diff_values[i] / bin_size)
                    if index == len(COLORS):
                        index -= 1
                    diff_mesh_colors[i] = COLORS[index]
                    changed = True

            if not changed:  # if hasn't changed, append to same list
                mesh.renderMaterial = ghosted
                if is_paired:
                    matched_previous_indices.append(paired_ref_mesh_index)
                same_meshes.append(mesh)

            else:  # set colors and add mesh to diff list or paired diff list
                diff_mesh.colors = diff_mesh_colors
                if is_paired:
                    diff_mesh_pairs.append(diff_mesh)
                    diff_mesh_ref_indices.append(paired_ref_mesh_index)
                else:
                    diff_meshes.append(diff_mesh)

        # process reference meshes
        diff_mesh_refs = []
        for j in range(0, len(previous_meshes)):
            # skip matched reference meshes and paired refs
            if matched_previous_indices.__contains__(j) or diff_mesh_ref_indices.__contains__(j):
                continue
            mesh = previous_meshes[j][0]
            mesh.renderMaterial = ghosted
            ref_meshes.append(mesh)
        for diff_mesh_ref_index in diff_mesh_ref_indices:
            mesh = previous_meshes[diff_mesh_ref_index]
            diff_mesh_refs.append(mesh[0])

        # Construct diff base object to return
        base = Base()
        base.units = current_meshes[0][0].units
        base["changed"] = diff_meshes
        for i in range(0, len(diff_mesh_pairs), 1):
            layer = f"changed::{i}"
            base[f"{layer}::changed"] = [diff_mesh_pairs[i]]
            base[f"{layer}::ref"] = [diff_mesh_refs[i]]
        base["same"] = same_meshes
        base["ref"] = ref_meshes
        return base

    @staticmethod
    def send_data(client: SpeckleClient, stream_id: str, branch: str, diff_object: Base, message: str) -> str:
        """Sends a Base object to a specified branch"""
        # create a branch if necessary
        branches = client.branch.list(stream_id)
        has_res_branch = any(b.name == branch for b in branches)

        if not has_res_branch:
            client.branch.create(
                stream_id, name=branch, description="This branch was created by the AEC Tech Masterclass App"
            )

        transport = ServerTransport(
            client=client, stream_id=stream_id)

        object_id = operations.send(base=diff_object, transports=[transport])

        commit_id = client.commit.create(
            stream_id,
            object_id,  # object id
            branch,
            message
        )

        return commit_id

    @staticmethod
    def receive_data(client: SpeckleClient, stream_id: str, commit_id: str) -> Base:
        """Get the data from a commit on the Speckle server"""
        transport = ServerTransport(stream_id, client)

        commit = client.commit.get(stream_id, commit_id)
        res = operations.receive(commit.referencedObject, transport)

        # if grasshopper, will be nested under data: res["data"]
        # if rhino/autocad/revit, will be sent with layers or categories

        return res

    @staticmethod
    def get_all_meshes(child: Base) -> List[Mesh]:
        """Returns all the meshes from a given Base object."""
        meshes = []

        names = child.get_dynamic_member_names()
        for name in names:
            prop = child[name]
            if isinstance(prop, Base):
                if isinstance(prop, Brep):
                    if not hasattr(prop, "displayMesh"):
                        break
                    meshes.append((prop.displayMesh, prop.id,
                                   prop.applicationId, prop))
                elif isinstance(prop, Mesh):
                    meshes.append((prop, prop.id, prop.applicationId))
            elif isinstance(prop, list):
                for p in prop:
                    if isinstance(p, Brep):
                        if not hasattr(p, "displayMesh"):
                            break
                        meshes.append(
                            (p.displayMesh, p.id, p.applicationId, p))
                    elif isinstance(p, Mesh):
                        meshes.append((p, p.id, p.applicationId))
                    elif hasattr(p, "displayMesh") or hasattr(p, "@displayMesh"):
                        meshes.append((p.displayMesh, p.id, p.applicationId))

        return meshes

    @staticmethod
    def get_all_points(meshes: List[Mesh]) -> List[Point]:
        """Returns a flat list of vertices of all the meshes in a list"""
        points = []
        for mesh in meshes:
            for i in range(2, len(mesh.vertices), 3):
                point = Point()
                point.x = mesh.vertices[i-2]
                point.y = mesh.vertices[i-1]
                point.z = mesh.vertices[i]
                points.append(point)
        return points

    @staticmethod
    def find_closest_point(current: Point, points: List[Point]):
        """Find the closest point to a target given a list of points"""
        smallest_distance = None
        for point in points:
            d = ((current.x - point.x)**2 + (current.y - point.y)
                 ** 2 + (current.z - point.z)**2)**0.5
            if smallest_distance is not None:
                if d > smallest_distance:
                    continue
            smallest_distance = d
        return smallest_distance
