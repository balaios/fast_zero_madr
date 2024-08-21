from fastapi import FastAPI

from fast_zero_madr.routes import auth, livro, romancista, users

app = FastAPI()

app.include_router(auth.router)
app.include_router(livro.router)
app.include_router(users.router)
app.include_router(romancista.router)
