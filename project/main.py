from fastapi import FastAPI
from .routers import products, jobs
from .database import Base, engine
from .models import job

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(products.router)
app.include_router(jobs.router)