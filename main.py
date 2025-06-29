
import os
from fastapi import FastAPI, HTTPException, Query
from dotenv import load_dotenv
from notion_client import Client
from typing import Optional, Dict, Any
from datetime import datetime

load_dotenv()
NOTION_SECRET = os.getenv("NOTION_SECRET")
notion = Client(auth=NOTION_SECRET)
app = FastAPI()

DATABASES = {
    "tareas": "1f863cd6-1526-802c-b0bf-f4e3a94fbc8a",
    "contratistas": "1f863cd6-1526-8143-9dc2-d6fb2d2d2c76",
    "clientes": "1f963cd6-1526-80ac-95b7-eefa1d6276f7",
    "llamadas": "1f963cd6-1526-8091-95af-ff85cb08931f",
    "juntas": "1fb63cd6-1526-80f5-a302-f2307123121d",
    "obras": "1f863cd6-1526-802f-941e-c528490f6e97",
    "equipo": "1f963cd6-1526-805b-814c-dfe52a247f63",
    "solicitudes_pago": "1fd63cd6-1526-8013-ad34-e55a18ee5d9b"
}

def limpiar_valor(valor: Dict[str, Any]) -> Any:
    tipo = valor.get("type")
    if tipo == "title":
        return valor["title"][0]["plain_text"] if valor["title"] else ""
    elif tipo == "rich_text":
        return valor["rich_text"][0]["plain_text"] if valor["rich_text"] else ""
    elif tipo == "date":
        return valor["date"]["start"] if valor["date"] else ""
    elif tipo == "select":
        return valor["select"]["name"] if valor["select"] else ""
    elif tipo == "multi_select":
        return [v["name"] for v in valor["multi_select"]]
    elif tipo == "people":
        return [p["name"] for p in valor["people"]]
    elif tipo == "relation":
        return [r["id"] for r in valor["relation"]]
    elif tipo == "checkbox":
        return valor["checkbox"]
    elif tipo == "email":
        return valor["email"]
    elif tipo == "phone_number":
        return valor["phone_number"]
    return valor.get(tipo, "")

@app.get("/consultar/{nombre_base}")
def consultar(nombre_base: str, filtro: Optional[str] = None, valor: Optional[str] = None):
    if nombre_base not in DATABASES:
        raise HTTPException(status_code=404, detail="Base de datos no encontrada")
    db_id = DATABASES[nombre_base]
    try:
        filtro_notion = {}
        if filtro and valor:
            filtro_notion = {
                "filter": {
                    "property": filtro,
                    "rich_text": {
                        "contains": valor
                    }
                }
            }
        response = notion.databases.query(database_id=db_id, **filtro_notion)
        datos = []
        for r in response["results"]:
            registro = {}
            for prop, val in r["properties"].items():
                registro[prop] = limpiar_valor(val)
            datos.append(registro)
        return {"resultados": datos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/crear/{nombre_base}")
def crear_entrada(nombre_base: str, propiedades: Dict[str, Any]):
    if nombre_base not in DATABASES:
        raise HTTPException(status_code=404, detail="Base de datos no encontrada")
    db_id = DATABASES[nombre_base]
    try:
        propiedades_formateadas = {
            k: {"rich_text": [{"text": {"content": str(v)}}]} for k, v in propiedades.items()
        }
        notion.pages.create(parent={"database_id": db_id}, properties=propiedades_formateadas)
        return {"mensaje": "Entrada creada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
