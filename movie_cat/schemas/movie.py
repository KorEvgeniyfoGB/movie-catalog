from datetime import datetime

from pydantic import BaseModel, Field, PositiveInt


class MovieBase(BaseModel):
    id: int
    title: str = Field(
        min_length=1,
        max_length=120,
    )
    description: str | None = Field(default=None, min_length=1, max_length=600)
    duration: PositiveInt | None = None
    kp_url: str | None = None


class Movie(MovieBase):
    """
    Модель фильма
    """
