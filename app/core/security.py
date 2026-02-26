from datetime import timedelta, datetime
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import select
import jwt
from jwt.exceptions import InvalidTokenError
from app.db.database import SessionDep
from app.core import config
from app.models import models


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

SECRET_KEY = f"{config.settings.secret_key}"

ALGORITHMS = f"{config.settings.algorithm}"

ACCESS_TOKEN_EXPIRE_MINUTES = config.settings.access_token_expire_minutes


#CREATE TOKEN
def create_access_token(data: dict, expire_time: timedelta | None):
    to_encode = data.copy()

    if expire_time:
        expire = datetime.now() + expire_time
    else:
        expire = datetime.now() + timedelta(minutes= 30)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHMS)
    return encoded_jwt

#VERIFY TOKEN
def verify_access_token(token: str, credential_exception):

    try:
        decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHMS])
        user_id: int = decoded_jwt.get("user_id")
        if not user_id:
            raise credential_exception
        
        token_data = models.TokenData(id=user_id)
    except InvalidTokenError:
        raise credential_exception
    
    return token_data

#USER VERIFY
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: SessionDep):
    credential_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "User was not validated", headers={"WWW-Authenticate": "Bearer"})

    user_token = verify_access_token(token, credential_exception)
    query = select(models.UserBase).where(models.UserBase.id == user_token.id)
    user = db.exec(query).first()

    if not user:
        raise credential_exception
    
    return user

# def user_login(data: Annotated[OAuth2PasswordRequestForm, Depends()], db: SessionDep):
#     query = select(models.UserBase).where(models.UserBase.username == data.username)
#     user = db.exec(query).first()
#     password = helpers.verify_password(data.password, user.password)

#     if not user:
#         raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "Invalid Credentials")
    
#     if not password:
#         raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "Invalid Credentials")
    
#     token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data= {"user_id": user.id}, expire_time= token_expire
#     )
#     return models.Token(access_token=access_token, token_bearer="bearer")