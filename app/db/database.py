from sqlmodel import Session, SQLModel, create_engine
from fastapi import Depends
from typing import Annotated
from app.core import config


sqlite_url = f"sqlite:///{config.settings.sqlite_file_name}"

engine = create_engine(sqlite_url)

def create_db_and_table():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]