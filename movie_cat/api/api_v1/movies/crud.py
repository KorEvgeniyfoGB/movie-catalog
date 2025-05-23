import logging

from pydantic import BaseModel, AnyHttpUrl, ValidationError

from schemas.movie import (
    Movie,
    MovieCreate,
    MovieUpdate,
    MovieUpdatePartial,
)

from core.config import MOVIE_STORAGE_FILE_PATH


# MOVIE_LIST = [
#     Movie(
#         slug="clue",
#         title="Clue",
#         description="Шесть гостей приезжают на светский ужин в загородный особняк, где их встречает дворецкий "
#         "Уодсворт. Приглашенные незнакомы ни друг с другом, ни с хозяином дома, которого вскоре кто-то "
#         "убивает.",
#         duration=94,
#         kp_url="https://www.kinopoisk.ru/film/14940/",
#     ),
#     Movie(
#         slug="murder_by_death",
#         title="Murder by Death",
#         description="Миллионер Лайонел Твейни приглашает на ужин в свой замок пятерых самых знаменитых детективов "
#         "мира: Сиднея Вана из Китая, Дика Чарльстона из Нью-Йорка, Джессику Марблс из Англии, "
#         "Майло Перье из Бельгии, Сэма Даймонда из Сан-Франциско. И надо же такому случиться, "
#         "что во время ужина появляется мистер Твейни и сообщает, что ровно в полночь в замке произойдет "
#         "убийство. Он предлагает миллион долларов тому, кто раскроет это преступление. Но за час до "
#         "полуночи обнаруживают труп слепого слуги мистера Твейни.",
#         duration=95,
#     ),
# ]

log = logging.getLogger(__name__)


class MovieStorage(BaseModel):
    slug_to_movie: dict[str, Movie] = {}

    def save_state(self) -> None:
        MOVIE_STORAGE_FILE_PATH.write_text(self.model_dump_json(indent=4))
        log.info("Saved movie to storage file.")

    @classmethod
    def from_state(cls) -> "MovieStorage":
        if not MOVIE_STORAGE_FILE_PATH.exists():
            log.info("Movie file doesn't exist.")
            return MovieStorage()
        return cls.model_validate_json(MOVIE_STORAGE_FILE_PATH.read_text())

    def init_storage_from_state(self):
        try:
            data = MovieStorage.from_state()
        except ValidationError:
            self.save_state()
            log.warning("Rewritten storage file due to validation error.")
            return
        self.slug_to_movie.update(
            data.slug_to_movie,
        )
        log.warning("Recovered data from storage file.")

    def get(self) -> list[Movie]:
        return list(self.slug_to_movie.values())

    def get_by_slug(self, slug: str) -> Movie:
        return self.slug_to_movie.get(slug)

    def create(self, movie_in: MovieCreate) -> Movie:
        movie = Movie(**movie_in.model_dump())
        self.slug_to_movie[movie.slug] = movie
        log.info("Movie with title %r created.", movie.title)
        return movie

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_movie.pop(slug, None)

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(movie.slug)
        log.info("Movie with title %r deleted.", movie.title)

    def update(
        self,
        movie: Movie,
        movie_in: MovieUpdate,
    ) -> Movie:
        for field_name, value in movie_in:
            setattr(movie, field_name, value)
        return movie

    def update_partial(
        self,
        movie: Movie,
        movie_in: MovieUpdatePartial,
    ) -> Movie:
        for field_name, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field_name, value)
        return movie


storage = MovieStorage()


# storage.create(
#     MovieCreate(
#         slug="clue",
#         title="Clue",
#         description="Шесть гостей приезжают на светский ужин в загородный особняк, где их встречает дворецкий "
#         "Уодсворт. Приглашенные незнакомы ни друг с другом, ни с хозяином дома, которого вскоре кто-то "
#         "убивает.",
#         duration=94,
#         kp_url=AnyHttpUrl("https://www.kinopoisk.ru/film/14940/"),
#     )
# )
#
# storage.create(
#     MovieCreate(
#         slug="murder_by_death",
#         title="Murder by Death",
#         description="Миллионер Лайонел Твейни приглашает на ужин в свой замок пятерых самых знаменитых детективов "
#         "мира: Сиднея Вана из Китая, Дика Чарльстона из Нью-Йорка, Джессику Марблс из Англии, "
#         "Майло Перье из Бельгии, Сэма Даймонда из Сан-Франциско. И надо же такому случиться, "
#         "что во время ужина появляется мистер Твейни и сообщает, что ровно в полночь в замке произойдет "
#         "убийство. Он предлагает миллион долларов тому, кто раскроет это преступление. Но за час до "
#         "полуночи обнаруживают труп слепого слуги мистера Твейни.",
#         duration=95,
#         kp_url=None,
#     )
# )
