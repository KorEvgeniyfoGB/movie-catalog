from fastapi import (
    APIRouter,
)
from starlette import status

from api.api_v1.movies.crud import storage
from schemas.movie import (
    Movie,
    MovieCreate,
    MovieOutput,
)

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get(
    "/",
    response_model=list[MovieOutput],
)
def read_movies_list():
    return storage.get()


@router.post(
    "/",
    response_model=MovieOutput,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(movie_create: MovieCreate):
    return storage.create(movie_in=movie_create)
