from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import requests

app = FastAPI()

# Підключення статичних файлів
app.mount("/static", StaticFiles(directory="static"), name="static")

# Підключення шаблонів
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

@app.get("/rates", response_class=HTMLResponse)
async def rates(request: Request):
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url)
    data = response.json()
    return templates.TemplateResponse(
        "rates.html", {"request": request, "rates": data["rates"], "base_currency": data["base"]}
    )

@app.get("/exchange", response_class=HTMLResponse)
async def exchange(request: Request):
    return templates.TemplateResponse("exchange.html", {"request": request})
