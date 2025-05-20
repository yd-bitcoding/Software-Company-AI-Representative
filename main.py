from fastapi import FastAPI
from routes import conversation_route
from database_utility.db_connection import init_db, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/", tags=["Welcome"])
def startup():
    init_db()
    return {"message": "Welcome to the AI Representative COnversation"}

app.include_router(conversation_route.router, prefix="/conversations", tags=["conversations"])


