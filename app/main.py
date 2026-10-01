from fastapi import FastAPI

from app.database.database import (
    Base,
    engine
)

from app.routers.auth import router as auth_router

from app.routers.todos import router as todo_router


# Create tables

Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="FastAPI Todo Application",
    version="1.0.0"
)


# Routers

app.include_router(
    auth_router
)

app.include_router(
    todo_router
)


@app.get("/")
def home():

    return {
        "message": "Todo API Running"
    }