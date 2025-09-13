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
        query=select(WorkPlanFact.type_product).distinct()
        type_products = session.execute(query).scalars().all()

    return templates.TemplateResponse("index.html", {"request": request, "type_products" : type_products})

app.include_router(router_prediction)
app.include_router(router_test_prediction)

uvicorn.run(app)
