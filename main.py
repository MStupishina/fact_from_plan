from fastapi import FastAPI, status, HTTPException
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from sqlalchemy import select

from app import *
from app.data_base.models import WorkPlanFact
from app.data_base.session import SessionLocal

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/hello")
def say_hello(name: str = "World"):
    return {"message": f"Hello, {name}!"}


@app.get("/")
def index(request: Request):
    type_products = []
    with SessionLocal() as session:
        query_tp = select(WorkPlanFact.type_product).distinct()
        type_products = session.execute(query_tp).scalars().all()
        query_pj = select(WorkPlanFact.project).distinct()
        projects = session.execute(query_pj).scalars().all()
        query_tw = select(WorkPlanFact.type_work_name).distinct()
        type_work_names = session.execute(query_tw).scalars().all()
        query_fn = select(WorkPlanFact.functional_name).distinct()
        functional_names = session.execute(query_fn).scalars().all()
        query_td = select(WorkPlanFact.type_doc_new).distinct()
        type_docs_new = session.execute(query_td).scalars().all()
        query_vd = select(WorkPlanFact.view_doc_new).distinct()
        view_docs_new = session.execute(query_vd).scalars().all()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "type_products": type_products,
        "projects": projects,
        "type_work_names": type_work_names,
        "functional_names": functional_names,
        "type_docs_new": type_docs_new,
        "view_docs_new": view_docs_new
    })


app.include_router(router_prediction)
app.include_router(router_test_prediction)

uvicorn.run(app)
