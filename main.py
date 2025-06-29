import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()
notion = Client(auth=os.getenv("NOTION_SECRET"))

# Mapear tipos básicos a texto
def get_prop_text(prop):
    t = prop["type"]
    try:
        if t == "title":
            return prop["title"][0]["plain_text"] if prop["title"] else ""
        elif t == "rich_text":
            return prop["rich_text"][0]["plain_text"] if prop["rich_text"] else ""
        elif t == "date":
            return prop["date"]["start"] if prop["date"] else ""
        elif t == "select":
            return prop["select"]["name"] if prop["select"] else ""
        elif t == "multi_select":
            return ", ".join([item["name"] for item in prop["multi_select"]])
        elif t == "people":
            return ", ".join([p["name"] for p in prop["people"]])
        elif t == "relation":
            # Obtener nombre de cada ID relacionada (requiere consulta adicional)
            names = []
            for rel in prop["relation"]:
                page = notion.pages.retrieve(rel["id"])
                title = page["properties"].get("Name") or page["properties"].get("Nombre")
                if title and title.get("title"):
                    names.append(title["title"][0]["plain_text"])
            return ", ".join(names)
        elif t == "checkbox":
            return "✅" if prop["checkbox"] else "❌"
        elif t == "email":
            return prop["email"] or ""
        elif t == "phone_number":
            return prop["phone_number"] or ""
        elif t == "number":
            return str(prop["number"]) if prop.get("number") is not None else ""
        else:
            return str(prop.get(t, ""))
    except:
        return "(error leyendo campo)"

def listar_registros(db_id):
    res = notion.databases.query(**{"database_id": db_id, "page_size": 100})
    for i, r in enumerate(res["results"], 1):
        print(f"\n=== Registro {i} ===")
        for name, prop in r["properties"].items():
            print(f"- {name}: {get_prop_text(prop)}")

def obtener_campos(db_id):
    res = notion.databases.retrieve(db_id)
    return {name: prop["type"] for name, prop in res["properties"].items()}

def crear_registro(db_id, data: dict):
    body = {"parent": {"database_id": db_id}, "properties": {}}
    for k, v in data.items():
        body["properties"][k] = v
    return notion.pages.create(**body)

def actualizar_registro(page_id, props: dict):
    return notion.pages.update(page_id=page_id, properties=props)

def main():
    print("Acciones disponibles:")
    print("1 - Listar campos")
    print("2 - Listar registros")
    print("3 - Crear nuevo registro")
    print("4 - Actualizar registro existente")
    opcion = input("Selecciona una opción (1-4): ").strip()

    db_id = input("Ingresa ID de la base de datos Notion: ").strip()
    try:
        if opcion == "1":
            campos = obtener_campos(db_id)
            print("\nCampos:")
            for n, t in campos.items():
                print(f"{n}: {t}")

        elif opcion == "2":
            listar_registros(db_id)

        elif opcion == "3":
            print("Formato de datos JSON. Ejemplo:")
            print('{"Nombre": {"title": [{"text": {"content": "Nueva Tarea"}}]}, "Prioridad": {"select": {"name": "Alta"}}}')
            raw = input("Datos: ")
            import json
            body = json.loads(raw)
            pag = crear_registro(db_id, body)
            print("Registro creado con ID:", pag["id"])

        elif opcion == "4":
            page_id = input("Ingresa ID de la página a actualizar: ").strip()
            print("Formato similar a creación. Ejemplo:")
            print('{"Estado": {"select": {"name": "En curso"}}}')
            raw = input("Datos: ")
            import json
            props = json.loads(raw)
            pag = actualizar_registro(page_id, props)
            print("Registro actualizado:", pag["id"])

        else:
            print("Opción no válida.")
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()
