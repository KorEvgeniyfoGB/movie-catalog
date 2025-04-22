from datetime import datetime
from typing import Annotated

from annotated_types import Len, MaxLen
from pydantic import BaseModel, Field, PositiveInt, AnyHttpUrl


class MovieBase(BaseModel):
    slug: str
    title: str
    description: str = ""
    duration: PositiveInt | str
    kp_url: AnyHttpUrl | None = None


class MovieCreate(MovieBase):
    """
    Модель для создания фильма
    """

    slug: Annotated[
        str,
        Len(min_length=3, max_length=20),
    ]
    title: Annotated[
        str,
        Len(min_length=1, max_length=120),
    ]
    description: Annotated[
        str,
        MaxLen(900),
    ] = ""
    duration: PositiveInt | str = "Неизвестно"


class Movie(MovieBase):
    """
    Модель фильма
    """
