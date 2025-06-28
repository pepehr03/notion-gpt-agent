import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
notion = Client(auth=NOTION_API_KEY)

def listar_registros(database_id):
    results = notion.databases.query(database_id=database_id, page_size=100).get("results", [])
    registros = []
    for page in results:
        props = page.get("properties", {})
        registro = {}
        for campo, valor in props.items():
            tipo = valor.get("type")
            if tipo == "title":
                texto = valor.get("title", [])
                registro[campo] = texto[0]["plain_text"] if texto else ""
            elif tipo == "rich_text":
                texto = valor.get("rich_text", [])
                registro[campo] = texto[0]["plain_text"] if texto else ""
            elif tipo == "number":
                registro[campo] = valor.get("number")
            elif tipo == "select":
                registro[campo] = valor.get("select", {}).get("name", "")
            elif tipo == "multi_select":
                registro[campo] = ", ".join([x["name"] for x in valor.get("multi_select", [])])
            elif tipo == "date":
                registro[campo] = valor.get("date", {}).get("start", "")
            elif tipo == "people":
                registro[campo] = ", ".join([p.get("name", "") for p in valor.get("people", [])])
            elif tipo == "email":
                registro[campo] = valor.get("email", "")
            elif tipo == "phone_number":
                registro[campo] = valor.get("phone_number", "")
            elif tipo == "checkbox":
                registro[campo] = "✅" if valor.get("checkbox") else "❌"
            elif tipo == "relation":
                registro[campo] = ", ".join([r.get("id", "") for r in valor.get("relation", [])])
            else:
                registro[campo] = f"[{tipo}]"
        registros.append(registro)
    return registros

def obtener_campos_base_datos(database_id):
    db = notion.databases.retrieve(database_id=database_id)
    props = db.get("properties", {})
    campos = {}
    for campo, val in props.items():
        campos[campo] = val.get("type", "desconocido")
    return campos
