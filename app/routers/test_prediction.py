from math import sqrt
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.utils import predict_test, predict_test_plus


router = APIRouter(tags=["test_prediction"])

class Works_test(BaseModel):
    work_test: int
    plan_labor: float

@router.post("/works_test", status_code=status.HTTP_201_CREATED)
def try_model_test(work_test: Works_test):
    result, fact = predict_test(work_test)
    if result:
        return {"fact_labor": fact}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=fact)

class Works_plus(BaseModel):
    work_plus: list[int]

@router.post("/works_plus", status_code=status.HTTP_201_CREATED)
def try_model_test(works_plus: Works_plus, start: int = None, end: int = None):
    fact=[]
    if works_plus.work_plus:
        fact += predict_test_plus(works_plus.work_plus)
    if start is not None and end is not None:
        fact += predict_test_plus(list(range(start,end+1)))


    mse=0
    for f in fact:
        mse += ( f['fact_labor_true']-f['fact_labor_predict'])**2
    rmse = sqrt(mse/len(fact))

    return {"fact_labor": fact, "RMSE": rmse}
