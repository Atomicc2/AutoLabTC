from fastapi import FastAPI

from api.rotas.automatos import router as automatos_router

app = FastAPI(title="AutoLabTC")

app.include_router(automatos_router, prefix="/automatos", tags=["automatos"])

@app.get("/")
def home():
    return {"message": "Olá, mundo!"}
