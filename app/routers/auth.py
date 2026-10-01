from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.models import UserDB
from app.schemas.schemas import (
    RegisterRequest,
    LoginRequest
)

from app.services.auth import (
    hash_password,
    verify_password,
    create_access_token
)

from app.services.rabbitmq import publish_email


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    user: RegisterRequest,
    db: Session = Depends(get_db)
):

    existing_user = (
        db.query(UserDB)
        .filter(
            UserDB.username == user.username
        )
        .first()
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )


    existing_email = (
        db.query(UserDB)
        .filter(
            UserDB.email == user.email
        )
        .first()
    )

    if existing_email:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )


    hashed_password = hash_password(
        user.password
    )


    new_user = UserDB(

        username=user.username,

        email=user.email,

        password_hash=hashed_password
    )


    db.add(new_user)

    db.commit()

    db.refresh(new_user)


    # Send email task to RabbitMQ
    publish_email(

        to_email=user.email,

        subject="Registration Successful",

        body=f"""
Hello {user.username},

Your account has been successfully created.

Welcome to our Todo Application!

Regards,
Todo Application
"""
    )


    return {

        "message": "Registration successful",

        "username": new_user.username,

        "email": new_user.email
    }


@router.post("/login")
def login(
    user: LoginRequest,
    db: Session = Depends(get_db)
):

    db_user = (

        db.query(UserDB)

        .filter(
            UserDB.username == user.username
        )

        .first()
    )


    if db_user is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )


    if not verify_password(
        user.password,
        db_user.password_hash
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )


    token = create_access_token(
        db_user.username
    )


    return {

        "access_token": token,

        "token_type": "Bearer"
    }