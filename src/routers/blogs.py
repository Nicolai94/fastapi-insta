from typing import Optional, List

from fastapi import APIRouter, Response, Query, Body, Depends
from starlette import status

from src._enum import BlogType
from src.schemas.blog_schema import BlogModel

blog_router = APIRouter(prefix="/blog", tags=["Blog"])


def required_functionality():
    return {"message": "learning FastAPI is important"}


@blog_router.get(
    "/all",
    summary="Retrieve all blogs",
    description="This api call simulates fetching all blogs",
    response_description="The lis of available blogs",
)
def get_all_blogs(
    page=1,
    page_size: Optional[int] = None,
    req_parameter: dict = Depends(required_functionality),
):
    return {"message": f"All {page_size} blogs on page {page}", "req": req_parameter}


@blog_router.get("/{id}/comments/{comment_id}")
def get_comment(
    id: int,
    comment_id: int,
    valid: bool = True,
    username: Optional[str] = None,
    req_parameter: dict = Depends(required_functionality),
):
    """ "
    Simulates fetching all comments
    - **id** mandatory path parameter
    """
    return {
        "message": f"blog_id {id}, comment_id {comment_id}, valid {valid}, username {username}"
    }


@blog_router.get("/type/{type}")
def get_blog_type(
    type: BlogType, req_parameter: dict = Depends(required_functionality)
):
    return {"message": f"Blog type {type.value}"}


@blog_router.get("/{id}")
def get_blog(id: int, response: Response):
    if id > 5:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": f"Blog {id} not found"}
    else:
        response.status_code = status.HTTP_200_OK
        return {"error": f"Blog with {id}"}


@blog_router.post("/new/{id}")
def create_blog(blog: BlogModel, id: int, version: int = 1):
    return {
        "id": id,
        "data": blog,
        "version": version,
    }


@blog_router.post("/new/{id}/comment")
def create_comment(
    blog: BlogModel,
    id: int,
    comment_id: int = Query(
        None,
        title="Id of the comment",
        description="Description of comment id",
        alias="commentId",
        deprecated=True,
    ),
    content: str = Body("hi how are you", min_length=10),
    v: Optional[List[str]] = Query(["1.0", "1.1", "1.2", "1.3", "1.4"]),
):
    return {
        "blog": blog,
        "id": id,
        "comment_id": comment_id,
        "content": content,
        "v": v,
    }
