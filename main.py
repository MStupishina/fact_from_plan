from fastapi import FastAPI, status, HTTPException
import uvicorn
from app import *

app = FastAPI()

@app.get("/hello")
def say_hello(name: str = "World"):
    return {"message": f"Hello, {name}!"}

app.include_router(router_prediction)
app.include_router(router_test_prediction)

uvicorn.run(app)
