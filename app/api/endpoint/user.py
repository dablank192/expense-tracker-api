from fastapi import APIRouter, Depends
from app.models import models
from app.repositories.user_repo import User
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix="/api/v1", tags=["Users"])

@router.post("/login", response_model= models.Token)
def login(data: Annotated[OAuth2PasswordRequestForm, Depends()], user: User = Depends()):
    users = user.user_login(data=data)
    return users

@router.post("/register", response_model= models.UserOut)
def create_user(data: models.UserCreate, user: User = Depends()):
    users = user.create_user(user= data)
    return users

@router.get("/users/{id}", response_model= models.UserOut)
def get_user(id: int, user: User = Depends()):
    users = user.get_user(id=id)
    return users