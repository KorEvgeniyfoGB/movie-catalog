from fastapi import HTTPException, BackgroundTasks
from starlette import status

from api.api_v1.movies.crud import storage
from schemas.movie import Movie


def prefetch_movie_by_slug(slug: str) -> Movie:
    movie: Movie | None = storage.get_by_slug(slug=slug)
    if movie:
        return movie
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie with slug {slug!r} not found",
    )


def save_state_storage(
    background_tasks: BackgroundTasks,
):
    yield
    background_tasks.add_task(storage.save_state)
