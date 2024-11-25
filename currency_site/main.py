from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
import requests
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve static files (CSS, JS, images, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up the Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Home route
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

# Rates route
@app.get("/rates", response_class=HTMLResponse)
async def rates(request: Request):
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url)
    data = response.json()

    rates = data['rates']
    base_currency = data['base']
    return templates.TemplateResponse("rates.html", {"request": request, "rates": rates, "base_currency": base_currency})

# Exchange route (GET for form, POST for processing)
@app.get("/exchange", response_class=HTMLResponse)
async def exchange_form(request: Request):
    return templates.TemplateResponse("exchange.html", {"request": request})

@app.post("/exchange", response_class=HTMLResponse)
async def exchange_result(request: Request, amount: float = Form(...), from_currency: str = Form(...), to_currency: str = Form(...)):
    base_currency = "USD"
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()
    rates = data['rates']

    conversion_result = None
    if from_currency in rates and to_currency in rates:
        conversion_rate = rates[to_currency] / rates[from_currency]
        conversion_result = amount * conversion_rate

    return templates.TemplateResponse("exchange.html", {
        "request": request,
        "rates": rates,
        "conversion_result": conversion_result,
        "amount": amount,
        "from_currency": from_currency,
        "to_currency": to_currency
    })
