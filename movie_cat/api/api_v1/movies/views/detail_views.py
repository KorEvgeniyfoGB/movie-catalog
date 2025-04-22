from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter
from starlette import status
from starlette.responses import RedirectResponse

from api.api_v1.movies.crud import storage
from api.api_v1.movies.dependencies import prefetch_movie_by_slug
from schemas.movie import Movie, MovieUpdate, MovieUpdatePartial

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

MovieBySlug = Annotated[
    Movie,
    Depends(prefetch_movie_by_slug),
]


@router.get(
    "/",
    response_model=Movie,
)
def read_movie_by_slug(
    movie: MovieBySlug,
) -> Movie:
    return movie


@router.put(
    "/",
    response_model=Movie,
)
def update_movie_detail(
    movie: MovieBySlug,
    movie_in: MovieUpdate,
) -> Movie:
    return storage.update(
        movie=movie,
        movie_in=movie_in,
    )


@router.patch(
    "/",
    response_model=Movie,
)
def update_movie_detail_partial(
    movie: MovieBySlug,
    movie_in: MovieUpdatePartial,
) -> Movie:
    return storage.update_partial(movie=movie, movie_in=movie_in)


@router.get("/kp/")
def redirect_to_kp(
    movie: MovieBySlug,
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
    movie: MovieBySlug,
) -> None:
    storage.delete(movie=movie)
