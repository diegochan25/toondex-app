from datetime import datetime
from pathlib import Path
from typing import Any
from fastapi import Request
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
from app.services import flash

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / 'templates'

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

def layout(path: str):  
    return f"layouts/{path}"


def macro(path: str):   
    return f"macros/{path}"


def partial(path: str): 
    return f"partials/{path}"


env.globals.update({
    'layout': layout,
    'macro': macro,
    'partial': partial,
    'now': datetime.now
})

templates = Jinja2Templates(env=env)

def _read_flash(request: Request) -> dict | None:
    if not flash.included(request):
        return None
    data = flash.read(request)
    return {'type': 'info', 'message': data} if isinstance(data, str) else data

def render(
    request: Request,
    filename: str,
    status_code: int = 200,
    headers: dict[str, str] = {},
    content_type: str | None = None,
    **context: Any,
):
    flash_data = _read_flash(request)
    response = templates.TemplateResponse(
        request,
        filename,
        {**context, 'flash': flash_data},
        headers=headers,
        status_code=status_code,
        media_type=content_type
    )
    if flash_data is not None:
        flash.clear(response)
    return response