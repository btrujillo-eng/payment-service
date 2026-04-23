from app.api.v1.routers import payment, health
from fastapi import FastAPI

app = FastAPI(
    title="Payment Processor API",
    version="1.0.0"
)

app.include_router(payment.router)
app.include_router(health.router)