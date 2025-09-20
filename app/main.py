from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()


app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.mount("/media", StaticFiles(directory=BASE_DIR / "media"), name="media")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
