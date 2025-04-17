from fastapi import HTTPException
from starlette import status

from api.api_v1.movies.crud import MOVIE_LIST
from schemas.movie import Movie


def prefetch_movie_by_id(id: int) -> Movie:
    movie: Movie | None = next(
        (movie for movie in MOVIE_LIST if movie.id == id),
        None,
    )
    if movie:
        return movie
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie with id {id} not found"
    )
