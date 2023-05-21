from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from sqlalchemy.orm import Session

from auth.oauth2 import get_current_user
from src.db.deps import get_db
from src.models.users import DBUser
from src.schemas.user_schema import UserBase, UserDisplay

users_router = APIRouter(prefix="/user", tags=["user"])


@users_router.post(
    "/create", response_model=UserDisplay, status_code=status.HTTP_201_CREATED
)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    hashed_password = pbkdf2_sha256.hash(request.password)
    new_user = DBUser(
        username=request.username, email=request.email, password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@users_router.get(
    "/all", response_model=List[UserDisplay], status_code=status.HTTP_200_OK
)
def get_all_users(
    db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)
):
    return db.query(DBUser).all()


@users_router.get("/{id}", response_model=UserDisplay)
def get_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserBase = Depends(get_current_user),
):
    user = db.query(DBUser).filter(DBUser.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@users_router.put("/{id}", response_model=UserDisplay)
def change_user(
    id: int,
    request: UserBase,
    db: Session = Depends(get_db),
    current_user: UserBase = Depends(get_current_user),
):
    hashed_password = pbkdf2_sha256.hash(request.password)
    user = db.query(DBUser).filter(DBUser.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    user.username = request.username
    user.password = hashed_password
    user.email = request.email
    db.commit()
    return user


@users_router.delete("/{id}")
def delete_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserBase = Depends(get_current_user),
):
    user = db.query(DBUser).filter(DBUser.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    db.delete(user)
    db.commit()
    return "Object was deleted"
