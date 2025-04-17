from typing import Annotated

from fastapi import Depends, APIRouter
from starlette.responses import RedirectResponse

from api.api_v1.movies.dependencies import prefetch_movie_by_id
from api.api_v1.movies.crud import MOVIE_LIST
from schemas.movie import Movie

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("/movies", response_model=list[Movie])
def read_movies_list():
    return MOVIE_LIST


@router.get("/movies/{id}", response_model=Movie)
def read_movie_by_id(movie: Annotated[Movie, Depends(prefetch_movie_by_id)]) -> Movie:
    return movie


@router.get("/movies/{id}/kp/")
def redirect_to_kp(movie: Annotated[Movie, Depends(prefetch_movie_by_id)]):
    return RedirectResponse(
        url=movie.kp_url,
    )
