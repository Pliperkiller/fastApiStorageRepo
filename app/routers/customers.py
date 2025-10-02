

from fastapi import HTTPException, status, APIRouter
from sqlmodel import select
from db import SessionDep
from models import Customer, CustomerCreate, CustomerUpdate

router = APIRouter()

@router.post("/customers", response_model=Customer,tags=["customers"])
async def create_customer(customer_data : CustomerCreate, session : SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)

    return customer

@router.get("/customers", response_model=list[Customer],tags=["customers"])
async def list_customer(session : SessionDep):
    return session.exec(select(Customer)).all()

@router.get("/customer/{customer_id}", response_model= Customer,tags=["customers"])
async def get_customer(customer_id : int, session : SessionDep):
    customer_response = session.get(Customer, customer_id)
    if not customer_response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Customer doesn't exist")
    return customer_response

@router.patch("/customer/{customer_id}", response_model= Customer, status_code=status.HTTP_201_CREATED,tags=["customers"])
async def update_customer(customer_id : int,customer_data : CustomerUpdate, session : SessionDep):
    customer_response = session.get(Customer, customer_id)
    if not customer_response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Customer doesn't exist")
    
    customer_dict = customer_data.model_dump(exclude_unset=True)

    customer_response.sqlmodel_update(customer_dict)
    session.add(customer_response)
    session.commit()
    session.refresh(customer_response)
    return customer_response

@router.delete("/customer/{customer_id}",tags=["customers"])
async def delete_customer(customer_id : int, session : SessionDep):
    customer_response = session.get(Customer, customer_id)
    if not customer_response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Customer doesn't exist")
    session.delete(customer_response)
    session.commit()
    return {"detail" : "ok"}