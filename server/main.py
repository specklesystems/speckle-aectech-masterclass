from typing import Optional
from fastapi import FastAPI, Request
from mesh_diff import compare_meshes
from fastapi.middleware.cors import CORSMiddleware

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


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/diff/{stream_id}/{commit_current}/{commit_previous}")
def get_diff(stream_id: str, commit_current: str, commit_previous: str, request: Request):
    print(request)
    print(request.headers.get("Authorisation"))
    token = request.headers.get("Authorisation").split(" ")[1]
    print(token)
    return compare_meshes(stream_id, commit_current, commit_previous, token)
