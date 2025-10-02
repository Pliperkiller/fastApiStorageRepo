from fastapi import FastAPI
from datetime import datetime
from models import Customer, Transaction, Invoice, CustomerCreate
from db import SessionDep, create_all_tables

import zoneinfo

app = FastAPI(lifespan=create_all_tables)

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
async def time(iso_code: str):
    
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"time": datetime.now(tz)}

@app.post("/customers", response_model=Customer)
async def create_customer(customer_data : CustomerCreate):
    customer = Customer.model_validate(customer_data.model_dump())
    customer.id = len(db_customers) + 1
    db_customers.append(customer)
    return customer

@app.get("/customers", response_model=list[Customer])
async def list_customer():
    return db_customers

@app.get("/customer/{customer_id}", response_model= Customer)
async def get_customer(customer_id : int):
    customer_response = next((customer for customer in db_customers if customer.id == customer_id), None)
    return customer_response

@app.post("/transactions")
async def create_transaction(transaction_data : Transaction):
    return transaction_data

@app.post("/invoices")
async def create_invoice(invoice_data : Invoice):
    return invoice_data
