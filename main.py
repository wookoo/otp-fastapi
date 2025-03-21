from fastapi import FastAPI
from domain.member import router as member_router

app = FastAPI()

app.include_router(member_router.router)
