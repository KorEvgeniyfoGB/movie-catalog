from fastapi import (
    APIRouter,
    BackgroundTasks,
)
from starlette import status

from api.api_v1.movies.crud import storage
from schemas.movie import (
    Movie,
    MovieCreate,
    MovieRead,
)

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get(
    "/",
    response_model=list[MovieRead],
)
def read_movies_list():
    return storage.get()


@router.post(
    "/",
    response_model=MovieRead,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(
    movie_create: MovieCreate,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(storage.save_state)
    return storage.create(movie_in=movie_create)
