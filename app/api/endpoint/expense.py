from fastapi import Depends, APIRouter, Query, status
from app.models_and_schemas import models
from app.core import security
from app.repositories import expense_repo
from typing import Annotated


router = APIRouter(prefix="/api/v1", tags=["Expenses"])


@router.get("/items", response_model= list[models.ExpenseOut])
def list_item(offset: int = 0, limit: Annotated[int, Query(le=100)] = 10, item: expense_repo.Expense = Depends(), current_user: models.UserOut = Depends(security.get_current_user)):
    items = item.list_item(offset=offset, limit=limit)
    return items

@router.get("/items/{id}", response_model= models.ExpenseOut)
def get_item(id: int, item: expense_repo.Expense = Depends(), current_user: models.UserOut = Depends(security.get_current_user)):
    items = item.get_item(id= id)
    return items

@router.post("/items", response_model= models.ExpenseOut)
def create_item(data: models.ExpenseCreate, current_user: models.UserOut = Depends(security.get_current_user), item: expense_repo.Expense = Depends()):
    items = item.create_item(data= data, user_id= current_user.id)
    return items

@router.patch("/items/{id}", response_model= models.ExpenseOut)
def update_item(id: int, data: models.ExpenseCreate, item: expense_repo.Expense = Depends(), current_user: models.UserOut = Depends(security.get_current_user)):
    items = item.update_item(id= id, user_id= current_user.id, data= data)
    return items

@router.delete("/items/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(id: int, item: expense_repo.Expense = Depends(), current_user: models.UserOut = Depends(security.get_current_user)):
    items = item.delete_item(id= id)
    return items