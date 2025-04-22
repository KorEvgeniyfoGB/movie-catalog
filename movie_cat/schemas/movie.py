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
    duration: PositiveInt | str = "Неизвестно"
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
    pass


class MovieUpdatePartial(MovieBase):
    title: TitleString | None = None
    description: DescriptionString | None = None
    duration: PositiveInt | str | None = None
    kp_url: AnyHttpUrl | None = None


class Movie(MovieBase):
    """
    Модель фильма
    """

    slug: str
