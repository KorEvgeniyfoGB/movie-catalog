from datetime import datetime
from typing import Annotated

from annotated_types import Len
from pydantic import BaseModel, Field, PositiveInt, AnyHttpUrl


class MovieBase(BaseModel):
    slug: str
    title: str
    description: str | None
    duration: PositiveInt | None = None
    kp_url: AnyHttpUrl | None = None


class MovieCreate(MovieBase):
    """
    Модель для создания фильма
    """

    slug: Annotated[str, Len(min_length=3, max_length=15)]
    title: Annotated[
        str,
        Len(min_length=1, max_length=120),
    ]
    description: (
        Annotated[
            str,
            Len(min_length=1, max_length=600),
        ]
        | None
    ) = None


class Movie(MovieBase):
    """
    Модель фильма
    """
