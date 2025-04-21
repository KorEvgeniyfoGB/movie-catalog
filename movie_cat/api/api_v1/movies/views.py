from random import randint
from typing import Annotated

from fastapi import (
    Depends,
    APIRouter,
    Form,
    HTTPException,
)
from starlette import status
from starlette.responses import RedirectResponse

from api.api_v1.movies.dependencies import prefetch_movie_by_slug
from api.api_v1.movies.crud import storage
from schemas.movie import Movie, MovieCreate

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get(
    "/",
    response_model=list[Movie],
)
def read_movies_list():
    return storage.get()


@router.post(
    "/",
    response_model=Movie,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(movie_create: MovieCreate):
    return storage.create(movie_in=movie_create)


@router.get(
    "/{slug}",
    response_model=Movie,
)
def read_movie_by_slug(
    movie: Annotated[
        Movie,
        Depends(prefetch_movie_by_slug),
    ],
) -> Movie:
    return movie


@router.get("/{slug}/kp/")
def redirect_to_kp(
    movie: Annotated[Movie, Depends(prefetch_movie_by_slug)],
) -> RedirectResponse:
    if movie.kp_url:
        return RedirectResponse(
            url=str(movie.kp_url),
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie with slug {movie.slug!r} not have link for kinopoisk.ru",
    )


@router.delete(
    "/{slug}/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Movie not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Movie slug not found",
                    },
                },
            },
        },
    },
)
def delete_movie_by_slug(
    movie: Annotated[
        Movie,
        Depends(prefetch_movie_by_slug),
    ],
) -> None:
    storage.delete(movie=movie)
