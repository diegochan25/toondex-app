from fastapi import APIRouter, Request
from app.config.templating import render

router = APIRouter(prefix='/admin')