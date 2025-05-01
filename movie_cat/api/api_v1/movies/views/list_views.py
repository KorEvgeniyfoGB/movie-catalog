from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
)
from starlette import status

from api.api_v1.movies.crud import storage
from api.api_v1.movies.dependencies import (
    save_state_storage,
    api_token_required,
)
from schemas.movie import (
    Movie,
    MovieCreate,
    MovieRead,
)

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
    dependencies=[
        Depends(save_state_storage),
        Depends(api_token_required),
    ],
)


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
):
    return storage.create(movie_in=movie_create)
