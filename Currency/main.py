from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()

# Вказуємо шлях до папки з HTML-шаблонами
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Отримуємо дані з API
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url)
    data = response.json()

    # Передаємо дані в шаблон
    return templates.TemplateResponse("index.html", {
        "request": request,
        "rates": data['rates'],
        "base_currency": data['base']
    })
