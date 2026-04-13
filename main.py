from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Procesador de Pagos V1 Online"}