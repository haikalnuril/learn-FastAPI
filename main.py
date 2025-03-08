from fastapi import FastAPI
from routers import users
from models import Base
from db_config import engine

def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}


