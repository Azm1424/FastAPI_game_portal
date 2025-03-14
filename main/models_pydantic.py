from pydantic import BaseModel, Field, EmailStr
from typing import List, Annotated
from datetime import date

class User(BaseModel):
    username: Annotated[str, Field(..., min_length=1, max_length=50, title='Username')]
    email: EmailStr
    password: Annotated[str, Field(..., min_length=5, title='Password')]

class Game(BaseModel):
    title: Annotated[str, Field(..., min_length=1, max_length=50, title='Title')]
    image: Annotated[str, Field(..., title='Image')]
    description: Annotated[str, Field(..., min_length=1, max_length=1000, title='Description')]
    genre: Annotated[str, Field(..., min_length=1, max_length=200, title='Genre')]
    rating_igdb: Annotated[float, Field(..., title='Rating_igdb')]
    trailer: Annotated[str, Field(..., title='Title')]
    platforms: Annotated[str, Field(..., min_length=1, max_length=100, title='Title')]
    avg_users_rating: Annotated[float, Field(..., title='Avg_users_rating')]

class Profile(BaseModel):
    username: Annotated[str, Field(..., min_length=1, max_length=50, title='Username')]
    name: Annotated[str, Field(..., min_length=1, max_length=50, title='Name')]
    age: Annotated[str, Field(..., min_length=1, max_length=50, title='Age')]
    country: Annotated[str, Field(..., min_length=1, max_length=50, title='Country')]
    city: Annotated[str, Field(..., min_length=1, max_length=50, title='City')]
    contacts: Annotated[str, Field(..., min_length=1, max_length=50, title='Your contacts')]
    favourite_game: Annotated[str, Field(..., min_length=1, max_length=50, title='Your favourite game')]

class Review(BaseModel):
    username: Annotated[str, Field(..., min_length=1, max_length=50, title='Username')]
    review: Annotated[str, Field(..., min_length=1, max_length=1000, title='Review')]
    rating: Annotated[int, Field(..., title='Rating')]
    created: Annotated[date, Field(..., title='Date')]