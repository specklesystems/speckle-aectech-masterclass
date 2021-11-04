"""FastAPI Backend for the AEC Tech Masterclass"""

import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mesh_diff import SpeckleMeshDiff


app = FastAPI()

server_url = os.environ.get("SPECKLE_SERVER", "https://speckle.xyz")
diff_branch = os.environ.get("DIFF_BRANCH", "diff")
frontend_url = os.environ.get("FRONTEND_URL", "http://localhost:8080")
origins = [
    "http://localhost",
    frontend_url,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/diff/{stream_id}/{commit_current}/{commit_previous}")
def get_diff(stream_id: str, commit_current: str, commit_previous: str, request: Request):
    """Diffing endpoint"""
    auth_header = request.headers.get("Authorisation")

    if auth_header is None:
        raise HTTPException(405, "No token provided")

    token = auth_header.split(" ")[1]

    try:
        mesh_differ = SpeckleMeshDiff(token, server_url, diff_branch)
        diff_commit = mesh_differ.process_diff(
            stream_id, commit_current, commit_previous)
    except Exception as e:
        print(e.with_traceback())
        raise HTTPException(500, e.with_traceback())
    return {"commit": diff_commit}


@app.get("/diff_check/{stream_id}/{commit_current}/{commit_previous}")
def get_diff_check(stream_id: str, commit_current: str, commit_previous: str, request: Request):
    """Diffing endpoint"""
    auth_header = request.headers.get("Authorisation")

    if auth_header is None:
        raise HTTPException(405, "No token provided")

    token = auth_header.split(" ")[1]

    try:
        mesh_differ = SpeckleMeshDiff(token, server_url, diff_branch)
        mesh_differ.stream_id = stream_id
        mesh_differ.commit_current = commit_current
        mesh_differ.commit_prev = commit_previous
        existing_diff_commit = mesh_differ.check_existing_commits()
        if existing_diff_commit is not None:

            return {"exists": True, "commit": existing_diff_commit}
        else:
            return {"exists": False, "commit": None}

    except Exception as e:
        print(e.with_traceback())
        raise HTTPException(500, e.with_traceback()))
