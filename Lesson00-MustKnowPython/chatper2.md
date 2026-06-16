### Typedict

TypedDict is used to define the expected structure of a dictionary, including its keys and value types.

from typing import TypedDict

class User(TypedDict):
    name: str
    age: int

user: User = {
    "name": "John",
    "age": 25
}