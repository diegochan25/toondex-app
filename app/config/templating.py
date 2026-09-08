from pathlib import Path
from typing import Any
from fastapi import Request
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader

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
    'partial': partial
})

templates = Jinja2Templates(env=env)

def render(
    request: Request, 
    filename: str, 
    status_code: int = 200,
    headers: dict[str, str] = {},
    content_type: str | None = None,
    **context: Any,
):
    return templates.TemplateResponse(
        request, 
        filename, 
        context,
        headers=headers,
        status_code=status_code,
        media_type=content_type
    )