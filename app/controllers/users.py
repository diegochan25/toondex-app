from uuid import UUID

from fastapi import APIRouter, HTTPException, Request
from app.config.templating import render
from app.dependencies import FromForm, RequiresDB, RequiresPagination
from app.schemas.admin import CreateUser, UpdateUser
from app.services import users


router = APIRouter(prefix='/users')

@router.get('/')
async def index(db: RequiresDB, request: Request, page: RequiresPagination):
    user_list = await users.all(db, page.limit, page.offset)
    return render(request, 'users/index.html.j2', users=user_list)

@router.get('/{id}')
async def show(db: RequiresDB, request: Request, id: str):
    try:
        uuid = UUID(id)
    except ValueError:
        raise HTTPException(400, detail="El parámetro 'id' no tuvo el formato correcto.")
    
    if (user := await users.find_by_id(db, uuid)) is None:
        raise HTTPException(404, detail='No se encontró un usuario con ese id.')
    
    return render(request, 'users/show.html.j2', user=user)

@router.post('/')
async def create(db: RequiresDB, data: FromForm[CreateUser]):
    pass

@router.get('/{id}/edit')
async def edit(db: RequiresDB, request: Request, id: str):
    return render(request, 'users/edit.html.j2')

@router.patch('/{id}')
async def update(id: str, data: FromForm[UpdateUser]):
    pass

@router.delete('/{id}')
async def destroy(id: str):
    pass
