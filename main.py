from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from notion_client import Client
import os

notion = Client(auth=os.getenv("NOTION_SECRET"))

DATABASE_IDS = {
    "solicitudes_pago": "1f...5d9b",
    "contratistas": "1f863cd6-1526-8143-9dc2-d6fb2d2d2c76",
    "clientes": "1f963cd6-1526-80ac-95b7-eefa1d6276f7",
    "tareas": "1f863cd6-1526-802c-b0bf-f4e3a94fbc8a",
    "llamadas": "1f963cd6-1526-8091-95af-ff85cb08931f",
    "juntas": "1fb63cd6-1526-80f5-a302-f2307123121d",
    "obras": "1f863cd6-1526-802f-941e-c528490f6e97",
    "equipo": "1f963cd6-1526-805b-814c-dfe52a247f63",
}

app = FastAPI()

class Filtro(BaseModel):
    property: str
    value: Any

class Propiedades(BaseModel):
    properties: Dict[str, Any]

@app.get("/consultar/{base}")
def consultar_base(base: str):
    if base not in DATABASE_IDS:
        raise HTTPException(404, f"Base '{base}' no encontrada")
    try:
        res = notion.databases.query(database_id=DATABASE_IDS[base], page_size=100)
        return res["results"]
    except Exception as e:
        raise HTTPException(500, f"Error al consultar: {e}")

@app.get("/campos/{base}")
def obtener_campos(base: str):
    if base not in DATABASE_IDS:
        raise HTTPException(404, f"Base '{base}' no encontrada")
    try:
        meta = notion.databases.retrieve(database_id=DATABASE_IDS[base])
        return meta["properties"]
    except Exception as e:
        raise HTTPException(500, f"Error al obtener campos: {e}")

@app.post("/filtrar/{base}")
def filtrar_base(base: str, filtro: Filtro):
    if base not in DATABASE_IDS:
        raise HTTPException(404, f"Base '{base}' no encontrada")
    try:
        res = notion.databases.query(
            database_id=DATABASE_IDS[base],
            filter={"property": filtro.property, "rich_text": {"contains": filtro.value}}
        )
        return res["results"]
    except Exception as e:
        raise HTTPException(500, f"Error al filtrar: {e}")

@app.post("/crear/{base}")
def crear_entrada(base: str, input: Propiedades):
    if base not in DATABASE_IDS:
        raise HTTPException(404, f"Base '{base}' no encontrada")
    try:
        nueva = notion.pages.create(
            parent={"database_id": DATABASE_IDS[base]},
            properties=input.properties
        )
        return nueva
    except Exception as e:
        raise HTTPException(500, f"Error al crear entrada: {e}")

@app.patch("/actualizar/{base}/{page_id}")
def actualizar_entrada(base: str, page_id: str, input: Propiedades):
    if base not in DATABASE_IDS:
        raise HTTPException(404, f"Base '{base}' no encontrada")
    try:
        updated = notion.pages.update(
            page_id=page_id,
            properties=input.properties
        )
        return updated
    except Exception as e:
        raise HTTPException(500, f"Error al actualizar: {e}")
