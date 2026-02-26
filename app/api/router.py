from fastapi import FastAPI, APIRouter
from app.api.endpoint import user, expense

api_router = APIRouter()

api_router.include_router(user.router)
api_router.include_router(expense.router)