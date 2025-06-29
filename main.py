import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()
NOTION_SECRET = os.getenv("NOTION_SECRET")
notion = Client(auth=NOTION_SECRET)

def obtener_campos_base_datos(database_id):
    try:
        response = notion.databases.retrieve(database_id)
        propiedades = response["properties"]
        campos = {nombre: propiedades[nombre]["type"] for nombre in propiedades}
        return campos
    except Exception as e:
        print("Error al obtener campos:", e)
        return None

def listar_registros(database_id):
    try:
        respuesta = notion.databases.query(database_id, page_size=100)
        registros = respuesta["results"]
        for i, registro in enumerate(registros, 1):
            print(f"\n======= Registro {i} =======")
            for propiedad, valor in registro["properties"].items():
                tipo = valor["type"]
                try:
                    if tipo == "title":
                        texto = valor["title"][0]["plain_text"] if valor["title"] else ""
                    elif tipo == "rich_text":
                        texto = valor["rich_text"][0]["plain_text"] if valor["rich_text"] else ""
                    elif tipo == "date":
                        texto = valor["date"]["start"] if valor["date"] else ""
                    elif tipo == "select":
                        texto = valor["select"]["name"] if valor["select"] else ""
                    elif tipo == "multi_select":
                        texto = ", ".join([v["name"] for v in valor["multi_select"]])
                    elif tipo == "people":
                        texto = ", ".join([p["name"] for p in valor["people"]])
                    elif tipo == "relation":
                        texto = ", ".join([r["id"] for r in valor["relation"]])
                    elif tipo == "checkbox":
                        texto = "✅" if valor["checkbox"] else "❌"
                    elif tipo == "email":
                        texto = valor["email"]
                    elif tipo == "phone_number":
                        texto = valor["phone_number"]
                    else:
                        texto = str(valor.get(tipo, ""))
                except Exception:
                    texto = "(error al leer valor)"
                print(f"{propiedad}: {texto}")
    except Exception as e:
        print("Error al listar registros:", e)

if __name__ == "__main__":
    db_id = input("Ingresa el ID de la base de datos de Notion: ")
    accion = input("¿Qué deseas hacer? (listar/campos): ").strip().lower()

    if accion == "listar":
        listar_registros(db_id)
    elif accion == "campos":
        campos = obtener_campos_base_datos(db_id)
        if campos:
            print("\nCampos de la base de datos:")
            for nombre, tipo in campos.items():
                print(f"- {nombre}: {tipo}")
    else:
        print("Acción no reconocida.")
