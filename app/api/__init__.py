from datetime import datetime

from fastapi import APIRouter
from app.api import v1


router = APIRouter(prefix='/api')

@router.get('/health', status_code=200)
def health():
    return {
        'status': 'ok',
        'service': 'toondex-app',
        'version': '0.1.0',
        'timestamp': datetime.now().isoformat()
    }

# @router.get('/ready')
# def ready(): 
#     pass

router.include_router(v1.router)