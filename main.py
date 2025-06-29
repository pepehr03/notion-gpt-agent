from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional
from notion_db import obtener_campos_base_datos, listar_registros
import os

app = FastAPI(title="Agente Notion GPT", version="1.0.0")

class Registro(BaseModel):
    base: str
    campo: Optional[str] = None
    valor: Optional[str] = None

BASES_DE_DATOS = {
    "tareas": "1f863cd6-1526-802c-b0bf-f4e3a94fbc8a",
    "solicitudes": "1fd63cd6-1526-8013-ad34-e55a18ee5d9b",
    "contratistas": "1f863cd6-1526-8143-9dc2-d6fb2d2d2c76",
    "clientes": "1f963cd6-1526-80ac-95b7-eefa1d6276f7",
    "llamadas": "1f963cd6-1526-8091-95af-ff85cb08931f",
    "juntas": "1fb63cd6-1526-80f5-a302-f2307123121d",
    "obras": "1f863cd6-1526-802f-941e-c528490f6e97",
    "equipo": "1f963cd6-1526-805b-814c-dfe52a247f63"
}

@app.get("/listar")
async def listar(base: str = Query(..., description="Nombre de la base de datos, ejemplo: tareas")):
    db_id = BASES_DE_DATOS.get(base.lower())
    if not db_id:
        return {"error": "Base de datos no reconocida"}
    return listar_registros(db_id)

@app.get("/campos")
async def campos(base: str = Query(..., description="Nombre de la base de datos")):
    db_id = BASES_DE_DATOS.get(base.lower())
    if not db_id:
        return {"error": "Base de datos no reconocida"}
    return obtener_campos_base_datos(db_id)
