import os
from io import BytesIO

import pandas as pd
from fastapi import APIRouter, HTTPException, status, UploadFile, File
from fastapi.responses import StreamingResponse

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

    out_buf = BytesIO()
    with pd.ExcelWriter(out_buf, engine="openpyxl") as writer:
        data.to_excel(writer, index=False)
    out_buf.seek(0)

    # отдаём как файл
    headers = {
        "Content-Disposition": "attachment; filename*=UTF-8''result.xlsx"
    }
    return StreamingResponse(
        out_buf,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers
    )

    # data.to_excel("result.xlsx", index=False)
    # file_new=FileResponse("result.xlsx", media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    # # if os.path.exists("result.xlsx"):
    # #     os.remove("result.xlsx")
    # return file_new