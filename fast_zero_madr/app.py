from fastapi import FastAPI

from fast_zero_madr.routes import auth, books, novelists, users

app = FastAPI()

app.include_router(auth.router)
app.include_router(books.router)
app.include_router(users.router)
app.include_router(novelists.router)
