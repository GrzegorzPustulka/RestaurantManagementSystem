import uvicorn
from fastapi import FastAPI

from admin_service.api.endpoints.category import router as category_router
from admin_service.api.endpoints.employee import router as employee_router
from admin_service.api.endpoints.menu import router as menu_router

app = FastAPI(
    title="Admin Service",
    description="This is the Admin Service for the DineStream application",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {"greeting": "Hello, World!", "message": "Welcome to FastAPI!"}


app.include_router(menu_router)
app.include_router(category_router)
app.include_router(employee_router)
