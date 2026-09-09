from fastapi import Request

from app.config.templating import render


async def not_found(request: Request, exc):
    if request.url.path.startswith('/admin/'):
        return render(request, 'not-found.html.j2', status_code=404)