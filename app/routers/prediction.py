from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.utils import predict

router = APIRouter(tags=["prediction"])

class Work(BaseModel):
    TYPE_PRODUCT: str
    PROJECT: str
    DIVISION_NAME: str
    STANDART_NAME: str
    DOC_TYPE_NAME: str
    TYPE_WORK_NAME: str
    FUNCTIONAL_NAME: str
    TYPE_DOC_NEW: str
    VIEW_DOC_NEW: str
    OPERPLAN_LABOR: float
    STANDART_LABOR: float
    PLAN_LABOR: float
    CASH: float

@router.post("/works", status_code=status.HTTP_201_CREATED)
def try_model(work: Work):
    result, fact = predict(work)
    if result:
        return {"fact_labor": fact}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=fact)
