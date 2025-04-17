from typing import Annotated
from fastapi import (
    FastAPI,
    Request,
    HTTPException,
    status,
    Depends,
)
from fastapi.responses import RedirectResponse
from schemas.movie import Movie

app = FastAPI(
    title="Movie Catalog",
)


@app.get("/")
def read_root(
    request: Request,
    name: str = "World",
):
    docs_url = request.url.replace(
        path="/docs",
        query="",
    )
    return {
        "message": f"Hello {name}",
        "docs": str(docs_url),
    }


MOVIE_LIST = [
    Movie(
        id=1,
        title="Clue",
        description="Шесть гостей приезжают на светский ужин в загородный особняк, где их встречает дворецкий "
        "Уодсворт. Приглашенные незнакомы ни друг с другом, ни с хозяином дома, которого вскоре кто-то "
        "убивает.",
        duration=94,
        kp_url="https://www.kinopoisk.ru/film/14940/",
    ),
    Movie(
        id=2,
        title="Murder by Death",
        description="Миллионер Лайонел Твейни приглашает на ужин в свой замок пятерых самых знаменитых детективов "
        "мира: Сиднея Вана из Китая, Дика Чарльстона из Нью-Йорка, Джессику Марблс из Англии, "
        "Майло Перье из Бельгии, Сэма Даймонда из Сан-Франциско. И надо же такому случиться, "
        "что во время ужина появляется мистер Твейни и сообщает, что ровно в полночь в замке произойдет "
        "убийство. Он предлагает миллион долларов тому, кто раскроет это преступление. Но за час до "
        "полуночи обнаруживают труп слепого слуги мистера Твейни.",
        duration=95,
    ),
]


@app.get("/movies", response_model=list[Movie])
def read_movies_list():
    return MOVIE_LIST


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


@app.get("/movies/{id}", response_model=Movie)
def read_movie_by_id(movie: Annotated[Movie, Depends(prefetch_movie_by_id)]) -> Movie:
    return movie


@app.get("/movies/{id}/kp/")
def redirect_to_kp(movie: Annotated[Movie, Depends(prefetch_movie_by_id)]):
    return RedirectResponse(
        url=movie.kp_url,
    )
