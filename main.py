from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

# Cargar variables de entorno
NOTION_SECRET = os.getenv("NOTION_SECRET")

# IDs de bases de datos desde Render
DBS = {
    "tareas": os.getenv("DB_TAREAS"),
    "contratistas": os.getenv("DB_CONTRATISTAS"),
    "clientes": os.getenv("DB_CLIENTES"),
    "llamadas": os.getenv("DB_LLAMADAS"),
    "juntas": os.getenv("DB_JUNTAS"),
    "obras": os.getenv("DB_OBRAS"),
    "equipo": os.getenv("DB_EQUIPO"),
    "solicitudes_pago": os.getenv("DB_SOLICITUDES_PAGO")
}

notion = Client(auth=NOTION_SECRET)
app = FastAPI()

class RegistroNuevo(BaseModel):
    propiedades: Dict[str, Any]

@app.get("/")
def raiz():
    return {"mensaje": "API funcionando correctamente"}

@app.get("/listar/{bd}")
def listar_registros(bd: str):
    if bd not in DBS or not DBS[bd]:
        raise HTTPException(status_code=404, detail="Base de datos no encontrada")
    try:
        respuesta = notion.databases.query(DBS[bd], page_size=100)
        return respuesta["results"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/campos/{bd}")
def obtener_campos(bd: str):
    if bd not in DBS or not DBS[bd]:
        raise HTTPException(status_code=404, detail="Base de datos no encontrada")
    try:
        bd_info = notion.databases.retrieve(DBS[bd])
        props = bd_info["properties"]
        return {k: props[k]["type"] for k in props}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/crear/{bd}")
def crear_registro(bd: str, entrada: RegistroNuevo):
    if bd not in DBS or not DBS[bd]:
        raise HTTPException(status_code=404, detail="Base de datos no encontrada")
    try:
        nuevo = notion.pages.create(
            parent={"database_id": DBS[bd]},
            properties=entrada.propiedades
        )
        return nuevo
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.patch("/actualizar/{page_id}")
def actualizar_registro(page_id: str, entrada: RegistroNuevo):
    try:
        actualizado = notion.pages.update(
            page_id=page_id,
            properties=entrada.propiedades
        )
        return actualizado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
