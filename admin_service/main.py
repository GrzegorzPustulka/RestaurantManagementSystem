from http.client import HTTPException

from fastapi import FastAPI, Request, HTTPException, status

from admin_service.api.external.category import router as category_router
from admin_service.api.external.employee import router as employee_router
from admin_service.api.external.menu import router as menu_router

from admin_service.api.internal.auth import router as auth_router

app = FastAPI(
    title="Admin Service",
    description="This is the Admin Service for the DineStream application",
    version="0.1.0",
)

app.include_router(menu_router)
app.include_router(category_router)
app.include_router(employee_router)
app.include_router(auth_router)


@app.middleware("http")
async def filter_requests(request: Request, call_next):
    if "/internal" in request.url.path:
        if "127.0.0.1" not in request.client.host:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden"
            )
    response = await call_next(request)
    return response


@app.get("/")
async def root():
    return {
        "message": "Welcome to the Admin Service! Please use the provided API documentation to interact with the service."
    }
