import uvicorn
from fastapi import FastAPI

from admin_service.api.endpoints.menu import router as menu_router
from admin_service.api.endpoints.category import router as category_router

app = FastAPI()


app.include_router(menu_router)
app.include_router(category_router)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")
