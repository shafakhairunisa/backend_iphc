from fastapi import FastAPI
from routes import disease_routes

app = FastAPI()

app.include_router(disease_routes.router, prefix="/api", tags=["diseases"])

@app.get("/")
def read_root():
    return {"Hello": "World"}