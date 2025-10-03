from fastapi import HTTPException, status, APIRouter
from sqlmodel import select

from db import SessionDep
from models import Plan, PlanCreate


router = APIRouter()


@router.post("/plans",tags=["plans"], status_code=status.HTTP_201_CREATED)
def create_plan(plan_data : PlanCreate, session : SessionDep):
    plan = Plan.model_validate(plan_data.model_dump())

    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan
    
@router.get("/plans", response_model=list[Plan],tags=["plans"])
def list_plans(session : SessionDep):
    return session.exec(select(Plan)).all()