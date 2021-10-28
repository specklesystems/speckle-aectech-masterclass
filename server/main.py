from typing import Optional
from fastapi import FastAPI
from mesh_diff import compare_meshes

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/diff/{stream_id}/{commit_current}/{commit_previous}")
def get_diff(stream_id: str, commit_current: str, commit_previous: str, q: Optional[str] = None):
    return compare_meshes(stream_id, commit_current, commit_previous)