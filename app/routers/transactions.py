from fastapi import HTTPException, status, APIRouter
from sqlmodel import select
from db import SessionDep
from models import Customer
from models import Transaction, TransactionCreate, TransactionUpdate

router = APIRouter()

@router.post("/transactions", status_code=status.HTTP_201_CREATED,tags=["transactions"])
async def create_transaction(transaction_data : TransactionCreate, session : SessionDep):
    
    transaction_dict = transaction_data.model_dump()
    customer = session.get(Customer, transaction_dict.get("customer_id"))
    if not customer:
            raise HTTPException(
                                status_code=status.HTTP_404_NOT_FOUND,
                                detail="Customer not found"
                                )
    transaction = Transaction.model_validate(transaction_dict)
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction

@router.get("/transactions",  response_model=list[Transaction] ,tags=["transactions"])
async def list_transactions(session : SessionDep):
    return session.exec(select(Transaction)).all()


@router.patch("/transactions/{transaction_id}", response_model=Transaction, tags=["transactions"])
async def update_transaction(transaction_id : int, transaction_data : TransactionUpdate, session : SessionDep):
    transaction_response = session.get(Transaction, transaction_id)
    if not transaction_response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Transaction doesn't exist")
    
    transaction_dict = transaction_data

    transaction_response.sqlmodel_update(transaction_dict)
    session.add(transaction_response)
    session.commit()
    session.refresh(transaction_response)
    return transaction_response

@router.delete("/transaction/{transtaction_id}",tags=["transactions"])
async def delete_transaction(transaction_id : int, session : SessionDep):
    transaction_response = session.get(Transaction, transaction_id)
    if not transaction_response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Transaction doesn't exist")
    session.delete(transaction_response)
    session.commit()
    return {"detail" : "ok"}
