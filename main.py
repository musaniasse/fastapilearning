from fastapi import FastAPI, HTTPException, Query, Body
from pydantic import BaseModel, AfterValidator, Field, HttpUrl
from typing  import Annotated, Literal


import random
app = FastAPI()

"""
"""

"""
FASTAPI attend un JSON en entrée et le client n'a qu'un seul paramètre de requête possible


class Image(BaseModel):
    url: HttpUrl
    name: str 

class Item(BaseModel):
    name: str
    description: str | None = None 
    price: float
    tax: float | None = None
    image: Image | None = None

@app.put("/items/{item_id}")
async def update_item(item_id: str, item: Annotated[Item, Body(embed=True)]):
    return {"item": item}
"""

"""
MODELE DE DONNEES POUR PARAMETRES DE REQUETES

class FilterParams(BaseModel):
    limit: int = Field(10, ge=1, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str]=[]


@app.get("/items/")
async def read_items(params: Annotated[FilterParams, Query()]):
    return params

PARAMETRES DE REQUETES


data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}

def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError('Invalid ID format, it must start with "isbn-" or "imdb-"')
    return id

@app.get("/items/")
async def read_items(id: Annotated[str | None, AfterValidator(check_valid_id)]=None):
    if not id:
        item = []
    if id:
        item = data.get(id)
    return {"id": id, "title": item}


@app.get("/items/{item_id}")
async def read_item( item_id: Annotated[str, AfterValidator(check_valid_id)]):
    if id:
        item = data.get(item_id)
    return {"item_id": item_id, "title": item}
    
"""

"""
CRUD operations for Users and Books using FastAPI.
"""

"""
class Book(BaseModel):
    id: int
    title: str

class User(BaseModel):
    user_id: int
    name: str
    age: int | None = None
    books: list[Book] | None = None

users_db: list[User] = []
books_db: list[Book] = []


@app.post("/user", response_model=User, status_code=201)
async def create_user(user: User):
    for existing_user in users_db:
        if existing_user.user_id == user.user_id:
            raise HTTPException(status_code=400, detail="User with this ID already exists")
    users_db.append(user)
    return user

@app.get("/users", response_model=list[User])
async def get_users():
    return users_db

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    for user in users_db:
        if user.user_id == user_id:
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{user_id}")
async def update_user(user_id: int, updated_user: User):
    for i, user in enumerate(users_db):
        if user.user_id == user_id:
            users_db[i] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    global users_db
    users_db = [u for u in users_db if u.user_id != user_id]
    return {"message": f"User {user_id} deleted successfully!"}

@app.get("/books", response_model=list[Book])
async def get_books():
    return books_db

@app.post("/books", response_model=Book, status_code=201)
async def create_book(book: Book):
    for i, ebook in enumerate(books_db):
        if ebook.id == book.id:
            raise HTTPException(status_code=400, detail=f"Book with this ID {book.id} already exists")
    books_db.append(book)
    return book
@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    for book in books_db:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found")

@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, updated_book: Book):
    for i, book in enumerate(books_db):
        if book.id == book_id:
            books_db[i] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found")

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    global books_db
    books_db = [book for book in books_db if book.id != book_id]
    return {"message": f"Book with ID {book_id} deleted successfully!"}

"""