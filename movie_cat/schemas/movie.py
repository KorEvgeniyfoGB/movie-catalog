from typing import Annotated

from annotated_types import Len, MaxLen
from pydantic import BaseModel, PositiveInt, AnyHttpUrl

DescriptionString = Annotated[
    str,
    MaxLen(900),
]

TitleString = Annotated[
    str,
    MaxLen(900),
]


class MovieBase(BaseModel):
    title: TitleString
    description: DescriptionString = ""
    duration: PositiveInt | str
    kp_url: AnyHttpUrl | None


class MovieCreate(MovieBase):
    """
    Модель для создания фильма
    """

    slug: Annotated[
        str,
        Len(min_length=3, max_length=20),
    ]
    title: TitleString
    description: DescriptionString = ""
    duration: PositiveInt | str = "Неизвестно"
    kp_url: AnyHttpUrl | None = AnyHttpUrl("https://www.kinopoisk.ru/")


class MovieUpdate(MovieBase):
    """
    Модель полного обновления фильма
    """

    duration: PositiveInt
    kp_url: AnyHttpUrl = AnyHttpUrl("https://www.kinopoisk.ru/")


class MovieUpdatePartial(MovieBase):
    """
    Модель частичного обновления фильма
    """

    title: TitleString | None = None
    description: DescriptionString | None = None
    duration: PositiveInt | str | None = None
    kp_url: AnyHttpUrl | None = None


class MovieRead(MovieBase):
    """
    Модель вывода фильма
    """

    slug: str


class Movie(MovieBase):
    """
    Модель фильма
    """

    slug: str
    notes: str

