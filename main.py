from fastapi import FastAPI

from app.api.v1.routers import health, payment

app = FastAPI(
    title="Payment Processor API",
    version="1.0.1"
)

app.include_router(payment.router)
app.include_router(health.router)