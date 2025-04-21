from pydantic import BaseModel, AnyHttpUrl

from schemas.movie import Movie, MovieCreate

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


class MovieStorage(BaseModel):
    slug_to_movie: dict[str, Movie] = {}

    def get(self) -> list[Movie]:
        return list(self.slug_to_movie.values())

    def get_by_slug(self, slug: str) -> Movie:
        return self.slug_to_movie.get(slug)

    def create(self, movie_in: MovieCreate) -> Movie:
        movie = Movie(**movie_in.model_dump())
        self.slug_to_movie[movie.slug] = movie
        return movie


storage = MovieStorage()

storage.create(
    MovieCreate(
        slug="clue",
        title="Clue",
        description="Шесть гостей приезжают на светский ужин в загородный особняк, где их встречает дворецкий "
        "Уодсворт. Приглашенные незнакомы ни друг с другом, ни с хозяином дома, которого вскоре кто-то "
        "убивает.",
        duration=94,
        kp_url=AnyHttpUrl("https://www.kinopoisk.ru/film/14940/"),
    )
)

storage.create(
    MovieCreate(
        slug="murder_by_death",
        title="Murder by Death",
        description="Миллионер Лайонел Твейни приглашает на ужин в свой замок пятерых самых знаменитых детективов "
        "мира: Сиднея Вана из Китая, Дика Чарльстона из Нью-Йорка, Джессику Марблс из Англии, "
        "Майло Перье из Бельгии, Сэма Даймонда из Сан-Франциско. И надо же такому случиться, "
        "что во время ужина появляется мистер Твейни и сообщает, что ровно в полночь в замке произойдет "
        "убийство. Он предлагает миллион долларов тому, кто раскроет это преступление. Но за час до "
        "полуночи обнаруживают труп слепого слуги мистера Твейни.",
        duration=95,
    )
)
