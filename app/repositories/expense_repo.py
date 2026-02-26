from sqlmodel import select
from app.db import database
from app.models import models
from fastapi import HTTPException, status

class Expense:
    def __init__(self, db: database.SessionDep):
        self.db = db
    
    def list_item(self, offset, limit):
        query = select(models.ExpenseBase).offset(offset).limit(limit)
        item = self.db.exec(query).all()
        return item
    
    def get_item(self, id: int):
        query = self.db.get(models.ExpenseBase, id)
        if not query:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "Item not found!")

        return query

    def create_item(self, data: models.ExpenseCreate, user_id: int):
        new_item = models.ExpenseBase(**data.model_dump())

        new_item.user_id = user_id
        
        self.db.add(new_item)
        self.db.commit()
        self.db.refresh(new_item)
        return new_item
    
    def update_item(self, id: int, user_id: int, data: models.Expense):
        query = self.db.get(models.ExpenseBase, id)

        if not query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Item's ID not found!")

        if query.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Item's ID not found!")
        
        item = data.model_dump(exclude_unset= True)
        query.sqlmodel_update(item)
        
        self.db.add(query)
        self.db.commit()
        self.db.refresh(query)
        return query

    def delete_item(self, id: int):
        query = self.db.get(models.ExpenseBase, id)
        if not query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Item's ID not found!")
        
        if id != query.user_id:
            raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "User is not allowed!")
        
        self.db.delete(query)
        self.db.commit()
        return {"msg":"Item deleted successfully!"}
