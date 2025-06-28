
from notion_client import Client

class NotionCustomClient:
    def __init__(self, token):
        self.client = Client(auth=token)

    def get_database_fields(self, database_id):
        try:
            db = self.client.databases.retrieve(database_id=database_id)
            properties = db.get("properties", {})
            return {k: v["type"] for k, v in properties.items()}
        except Exception as e:
            print("Error al obtener campos:", e)
            return {}

    def get_database_records(self, database_id):
        try:
            records = []
            response = self.client.databases.query(database_id=database_id, page_size=100)
            for result in response.get("results", []):
                record = {}
                props = result.get("properties", {})
                for key, value in props.items():
                    field_type = value.get("type")
                    if field_type == "title":
                        record[key] = value["title"][0]["plain_text"] if value["title"] else ""
                    elif field_type == "rich_text":
                        record[key] = value["rich_text"][0]["plain_text"] if value["rich_text"] else ""
                    elif field_type == "number":
                        record[key] = value.get("number", "")
                    elif field_type == "date":
                        record[key] = value["date"]["start"] if value["date"] else ""
                    elif field_type == "checkbox":
                        record[key] = "✅" if value.get("checkbox") else "❌"
                    elif field_type in ["select", "status"]:
                        record[key] = value[field_type]["name"] if value.get(field_type) else ""
                    elif field_type == "multi_select":
                        record[key] = ", ".join([opt["name"] for opt in value.get("multi_select", [])])
                    elif field_type == "email":
                        record[key] = value.get("email", "")
                    elif field_type == "phone_number":
                        record[key] = value.get("phone_number", "")
                    elif field_type == "relation":
                        related = value.get("relation", [])
                        record[key] = ", ".join([r.get("id", "") for r in related])
                    elif field_type == "people":
                        people = value.get("people", [])
                        record[key] = ", ".join([p.get("name", "") for p in people])
                    elif field_type == "created_time":
                        record[key] = value.get("created_time", "")
                    else:
                        record[key] = str(value.get(field_type, ""))
                records.append(record)
            return records
        except Exception as e:
            print("Error al obtener registros:", e)
            return []
