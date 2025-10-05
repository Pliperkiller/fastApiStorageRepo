import time
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Request, status
from datetime import datetime

from fastapi.security import HTTPBasic, HTTPBasicCredentials
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

security = HTTPBasic()

@app.get("/")
async def root(credentials : Annotated[HTTPBasicCredentials, Depends(security)]):
    print(credentials)
    if credentials.username == "ca" and credentials.password == "ro":
        return {"message":f"Hola,{credentials.username}"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

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
