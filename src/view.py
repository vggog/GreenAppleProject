from fastapi import APIRouter


router = APIRouter(
    prefix="/hello_world",
)


@router.get("/")
def hello_world_view():
    return "Hello world"
