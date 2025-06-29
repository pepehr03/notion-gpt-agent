from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from notion_client import Client
import os

# Inicializar cliente de Notion
notion = Client(auth=os.getenv("NOTION_SECRET"))

# IDs de tus bases de datos
DATABASE_IDS = {
    "solicitudes_pago": "1fd63cd6-1526-8013-ad34-e55a18ee5d9b",
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
    campo: str
    valor: Any

class NuevaEntrada(BaseModel):
    propiedades: Dict[str, Any]

@app.get("/consultar/{base}")
def consultar_base(base: str):
    if base not in DATABASE_IDS:
        raise HTTPException(status_code=404, detail="Base no encontrada")
    try:
        respuesta = notion.databases.query(database_id=DATABASE_IDS[base])
        return respuesta["results"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/filtrar/{base}")
def filtrar_base(base: str, filtro: Filtro):
    if base not in DATABASE_IDS:
        raise HTTPException(status_code=404, detail="Base no encontrada")
    try:
        respuesta = notion.databases.query(
            database_id=DATABASE_IDS[base],
            filter={"property": filtro.campo, "rich_text": {"contains": filtro.valor}}
        )
        return respuesta["results"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/crear/{base}")
def crear_entrada(base: str, entrada: NuevaEntrada):
    if base not in DATABASE_IDS:
        raise HTTPException(status_code=404, detail="Base no encontrada")
    try:
        nueva = notion.pages.create(
            parent={"database_id": DATABASE_IDS[base]},
            properties=entrada.propiedades
        )
        return nueva
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
