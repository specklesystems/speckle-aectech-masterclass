"""FastAPI Backend for the AEC Tech Masterclass"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import mesh_diff as md

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
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
    token = request.headers.get("Authorisation").split(" ")[1]
    md.authenticate(token)
    return md.compare_meshes(stream_id, commit_current, commit_previous)
