from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from app.config.templating import render
from app.dependencies import FromForm, RequiresDB, RequiresPagination
from app.models.users import UserGenders, UserRoles
from app.schemas.admin import CreateUser, UpdateUser
from app.services import flash, users


router = APIRouter(prefix='/users')


@router.get('/')
async def index(db: RequiresDB, request: Request, page: RequiresPagination):
    user_list = await users.all(db, page.limit, page.offset)
    return render(
        request,
        'users/index.html.j2',
        users=user_list,
        roles=UserRoles,
        genders=UserGenders
    )


@router.get('/{id}')
async def show(db: RequiresDB, request: Request, id: str):
    try:
        uuid = UUID(id)
    except ValueError:
        raise HTTPException(
            400, detail="El parámetro 'id' no tuvo el formato correcto.")

    if (user := await users.find_by_id(db, uuid)) is None:
        raise HTTPException(
            404, detail='No se encontró un usuario con ese id.')

    return render(request, 'users/show.html.j2', user=user)


@router.post('/', status_code=201)
async def create(request: Request, db: RequiresDB, data: Annotated[CreateUser, Form()]):
    exists = await users.exists_by_email(data.email)
    if exists:
        user_list = await users.all(db)
        return flash.send({ 
                'type': 'error', 
                'message': 'A user with this email already exists.' 
            }, response=render(
                request, 
                'users/index.html.j2',
                users=user_list,
                roles=UserRoles,
                genders=UserGenders
            )
        )

@router.get('/{id}/edit')
async def edit(db: RequiresDB, request: Request, id: str):
    return render(request, 'users/edit.html.j2')


@router.patch('/{id}')
async def update(id: str, data: FromForm[UpdateUser]):
    pass


@router.delete('/{id}')
async def destroy(id: str):
    pass
