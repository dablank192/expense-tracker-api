from app.db import database
from app.models_and_schemas import models
from fastapi import HTTPException, status
from app.utils import helpers
from sqlmodel import select
from datetime import timedelta
from app.core import security


class User:
    def __init__(self, db: database.SessionDep):
        self.db = db

    def create_user(self, user: models.UserCreate):
        hashed_password = helpers.get_password_hash(user.password)
        user.password = hashed_password

        users = models.UserBase(**user.model_dump())
        self.db.add(users)
        self.db.commit()
        self.db.refresh(users)
        return users
    
    def get_user(self, id: int):
        query = self.db.get(models.UserBase, id)
        if not query:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "User Not Found!")
        
        return query
    
    def user_login(self, data: str):
        query = select(models.UserBase).where(models.UserBase.username == data.username)
        user = self.db.exec(query).first()

        if not user:
            raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "Invalid Credentials")
        
        password = helpers.verify_password(data.password, user.password)

        if not password:
            raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "Invalid Credentials")
        
        token_expire = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = security.create_access_token(
            data= {"user_id": user.id}, expire_time= token_expire
        )
        return models.Token(access_token=access_token, token_bearer="bearer")