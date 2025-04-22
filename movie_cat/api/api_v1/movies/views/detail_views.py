from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter
from starlette import status
from starlette.responses import RedirectResponse

from api.api_v1.movies.crud import storage
from api.api_v1.movies.dependencies import prefetch_movie_by_slug
from schemas.movie import Movie


router = APIRouter(
    prefix="/{slug}",
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


@router.get(
    "/",
    response_model=Movie,
)
def read_movie_by_slug(
    movie: Annotated[
        Movie,
        Depends(prefetch_movie_by_slug),
    ],
) -> Movie:
    return movie


@router.get("/kp/")
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
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_movie_by_slug(
    movie: Annotated[
        Movie,
        Depends(prefetch_movie_by_slug),
    ],
) -> None:
    storage.delete(movie=movie)
