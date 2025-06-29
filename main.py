from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"mensaje": "API funcionando correctamente"}
Fix: agregar app para FastAPI
