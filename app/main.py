import time
from fastapi import FastAPI, Request
from datetime import datetime
from models import Customer, Invoice
from db import create_all_tables
from .routers import customers,transactions, plans

import zoneinfo

app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(plans.router)


@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    response.headers["Process-Time"] = str(process_time)
    return response


@app.get("/")
async def root():
    return {"message":"Hola,mundo"}

country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima",
}

db_customers : list[Customer] = []


@app.get("/time/{iso_code}")
async def get_time_by_iso(iso_code: str):
    
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"time": datetime.now(tz)}


@app.post("/invoices")
async def create_invoice(invoice_data : Invoice):
    return invoice_data
