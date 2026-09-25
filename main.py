from fastapi import FastAPI
from tasks import router

app=FastAPI()

app.include_router(router=router)