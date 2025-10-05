from fastapi import HTTPException, Query, status, APIRouter
from sqlmodel import select
from db import SessionDep
from models import Customer, CustomerCreate, CustomerPlan, CustomerUpdate, Plan, StatusEnum, Transaction

router = APIRouter()

@router.post("/customers", response_model=Customer,tags=["customers"], status_code=status.HTTP_201_CREATED)
async def create_customer(customer_data : CustomerCreate, session : SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)

    return customer

@router.get("/customers", response_model=list[Customer],tags=["customers"])
async def list_customer(session : SessionDep):
    return session.exec(select(Customer)).all()

@router.get("/customers/{customer_id}", response_model= Customer,tags=["customers"])
async def get_customer(customer_id : int, session : SessionDep):
    customer_response = session.get(Customer, customer_id)
    if not customer_response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Customer doesn't exist")
    return customer_response

@router.patch("/customers/{customer_id}", response_model= Customer, status_code=status.HTTP_201_CREATED,tags=["customers"])
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

@router.delete("/customers/{customer_id}",tags=["customers"])
async def delete_customer(customer_id : int, session : SessionDep):
    customer_response = session.get(Customer, customer_id)
    if not customer_response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Customer doesn't exist")
    session.delete(customer_response)
    session.commit()
    return {"detail" : "ok"}

@router.get("/transactions/{customer_id}",  response_model=list[Transaction] ,tags=["customers"])
async def list_transactoin_by_customer_id(customer_id : int , session: SessionDep):
    customer_db = session.get(Customer, customer_id)

    if not customer_db:
         raise HTTPException(
              status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
         )
    
    return customer_db.transactions

@router.post("/customers/{customer_id}/plans/{plan_id}",response_model= CustomerPlan,tags=["customers"])
async def susbscribe_customer_to_plan(customer_id : int, plan_id : int, session : SessionDep, plan_status : StatusEnum = Query()):
    customer_db = session.get(Customer, customer_id)
    plan_db = session.get(Plan, plan_id)

    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Customer doesnt exist")

    if not plan_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Plan doesnt exist")
    
    customer_plan = CustomerPlan(plan_id=plan_db.id, customer_id=customer_db.id, status= plan_status)
    session.add(customer_plan)
    session.commit()
    session.refresh(customer_plan)
    return customer_plan

#GET /customer/123/plans?plan_status=ACTIVE
@router.get("/customers/{customer_id}/plans", response_model=list[Plan],tags=["customers"])
async def get_suscriptions(customer_id : int, session : SessionDep, plan_status : StatusEnum = Query()):
    customer_db = session.get(Customer,customer_id)

    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Customer doesnt exist")
    query = select(CustomerPlan).where(CustomerPlan.customer_id == customer_id).where(CustomerPlan.status == plan_status)
    plans = session.exec(query).all()
    return plans