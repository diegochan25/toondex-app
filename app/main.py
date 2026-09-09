import uvicorn
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_tailwind import tailwind
from app import api, controllers
from app.core.handlers import not_found
from app.dependencies import get_settings


ROOT_DIR = Path(__file__).resolve().parent.parent
settings = get_settings()
static_files = StaticFiles(directory=str(ROOT_DIR / 'app' / 'static'))

@asynccontextmanager
async def lifespan(_: FastAPI):
    process = tailwind.compile(
        static_files.directory + '/css/output.css',
        tailwind_stylesheet_path=str(ROOT_DIR / 'app' / 'input.css'),
        watch=settings.python_env == 'development'
    )
    yield
    process.terminate()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=settings.allow_credentials,
    allow_methods=settings.allowed_methods,
    allow_headers=settings.allowed_headers
)

app.mount('/static', static_files, name='static')

app.include_router(api.router)
app.include_router(controllers.router)
app.add_exception_handler(404, not_found)

def main():
    uvicorn.run(
        'app.main:app',
        host=settings.app_host,
        port=settings.app_port,
        log_level=settings.log_level,
        reload=settings.python_env == 'development'
    )


if __name__ == '__main__':
    main()