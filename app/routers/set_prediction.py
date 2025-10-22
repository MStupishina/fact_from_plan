import os

import pandas as pd
from fastapi import APIRouter, HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse

from app.utils import predict_test, predict_test_plus


router = APIRouter(tags=["test_prediction"])

@router.post("/set_works", status_code=status.HTTP_201_CREATED)
async def set_works_try(file: UploadFile = File(...)):
    if not (file.filename.endswith(".xlsx") or file.filename.endswith(".xls")):
        raise HTTPException(status_code=400, detail="Ожидается excel файл")
    raw = await file.read()
    if len(raw) == 0:
        raise HTTPException(status_code=400, detail="Пустой файл")
    data = pd.read_excel(raw, engine="openpyxl")
    print(data)
    result = predict_test_plus(list(range(len(data))),data)
    fact=[]
    for i in result:
        fact.append(i['fact_labor_predict'])
    if "FACT_LABOR" in data.columns:
        data["FACT_LABOR_PREDICT"] = fact
    else:
        data["FACT_LABOR"] = fact
    data.to_excel("result.xlsx", index=False)
    file_new=FileResponse("result.xlsx", media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    # if os.path.exists("result.xlsx"):
    #     os.remove("result.xlsx")
    return file_new