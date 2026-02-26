from fastapi import FastAPI
from app.db.database import create_db_and_table
from app.api.router import api_router



app = FastAPI(
    title= "Expense-Tracker-API",
    version= "1.0.0"
)

@app.on_event("startup")
def on_startup():
    create_db_and_table()

app.include_router(api_router)