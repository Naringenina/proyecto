from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.db.session import init_db
from fastapi import Request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()

(BASE_DIR / "static").mkdir(parents=True, exist_ok=True)
(BASE_DIR / "media").mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.mount("/media", StaticFiles(directory=BASE_DIR / "media"), name="media")

templates = Jinja2Templates(directory=BASE_DIR / "templates")

@app.lifespan("startup")
def on_startup():
    init_db()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

