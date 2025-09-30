from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

router = APIRouter()

@router.get("/items", response_class=HTMLResponse)
def items_page(request: Request):
    return templates.TemplateResponse("items/list.html", {"request": request})

@router.get("/items/new", response_class=HTMLResponse)
def new_item_page(request: Request):
    return templates.TemplateResponse("items/new.html", {"request": request})

@router.get("/tags", response_class=HTMLResponse)
def tags_page(request: Request):
    return templates.TemplateResponse("tags.html", {"request": request})

@router.get("/import", response_class=HTMLResponse)
def import_page(request: Request):
    return templates.TemplateResponse("import.html", {"request": request})

@router.get("/export", response_class=HTMLResponse)
def export_page(request: Request):
    return templates.TemplateResponse("export.html", {"request": request})
