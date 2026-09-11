import json
from fastapi import HTTPException, Request, Response

FLASH_KEY = 'flash'

FLASH_COOKIE_ARGS = {
    'key': FLASH_KEY,
    'path': '/',
    'domain': None,
    'max_age': 10,
    'secure': True,
    'httponly': True,
    'samesite': 'none'
}

def send(data: str | dict, response: Response | None = None):
    payload = json.dumps(data)
    if response is None:
        response = Response()
    response.set_cookie(**FLASH_COOKIE_ARGS, value=payload)
    return response

def included(request: Request) -> bool:
    return request.cookies.get(FLASH_KEY) is not None

def read(request: Request) -> str | dict:
    flash = request.cookies.get(FLASH_KEY)
    if not flash:
        return ''
    try:
        return json.loads(flash)
    except json.JSONDecodeError as e:
        raise HTTPException('services.flash: Flash cookie\'s value is malformed.') from e

def clear(response: Response):
    response.delete_cookie(**FLASH_COOKIE_ARGS)