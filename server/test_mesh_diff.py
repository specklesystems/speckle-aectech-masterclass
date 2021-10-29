from mesh_diff import SpeckleMeshDiff
from specklepy.api.credentials import get_default_account

STREAM_ID = "8325294b8f"
COMMIT_ID = "c207299871"  # current commit
PREV_COMMIT_ID = "b9f376d75d"  # previous commit

account = get_default_account()
md = SpeckleMeshDiff(account.token)
md.process_diff(STREAM_ID, COMMIT_ID, PREV_COMMIT_ID)
