import uvicorn
from fastapi import FastAPI
from app import api, controllers
from app.dependencies import get_settings
from fastapi.middleware.cors import CORSMiddleware

settings = get_settings()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=settings.allow_credentials,
    allow_methods=settings.allowed_methods,
    allow_headers=settings.allowed_headers
)

app.include_router(api.router)
app.include_router(controllers.router)

if __name__ == '__main__':
    uvicorn.run(
        app, 
        host=settings.app_host, 
        port=settings.app_port,
        log_level=settings.log_level
    )