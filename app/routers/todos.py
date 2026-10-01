from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from fastapi.security import HTTPBearer

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.models import Todo

from app.schemas.schemas import (
    TodoCreate,
    TodoResponse
)

from app.services.auth import verify_token


router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)


security = HTTPBearer()


def get_current_user(
    credentials=Depends(security)
):

    token = credentials.credentials

    return verify_token(token)


@router.post(
    "/",
    response_model=TodoResponse
)
def create_todo(

    todo: TodoCreate,

    db: Session = Depends(get_db),

    current_user: str = Depends(
        get_current_user
    )
):

    new_todo = Todo(

        title=todo.title,

        description=todo.description,

        user_id=1
    )

    db.add(new_todo)

    db.commit()

    db.refresh(new_todo)

    return new_todo


@router.get(
    "/",
    response_model=list[TodoResponse]
)
def get_todos(

    db: Session = Depends(get_db),

    current_user: str = Depends(
        get_current_user
    )
):

    return db.query(Todo).all()


@router.delete("/{todo_id}")
def delete_todo(

    todo_id: int,

    db: Session = Depends(get_db),

    current_user: str = Depends(
        get_current_user
    )
):

    todo = (

        db.query(Todo)

        .filter(
            Todo.id == todo_id
        )

        .first()
    )


    if todo is None:

        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )


    db.delete(todo)

    db.commit()


    return {
        "message": "Todo deleted successfully",

        "deleted_by": current_user
    }