from fastapi import APIRouter, Request
from app.config.templating import render
from app.controllers import users

router = APIRouter(prefix='/admin')

@router.get('/')
def index(request: Request):
    return render(request, 'admin/index.html.j2')

router.include_router(users.router)