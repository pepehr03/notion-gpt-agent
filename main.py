from notion_db import listar_registros, obtener_campos_base_datos

if __name__ == "__main__":
    db_id = input("Ingresa el ID de la base de datos de Notion: ").strip()
    accion = input("¿Qué deseas hacer? (listar/campos): ").strip().lower()

    if accion == "listar":
        try:
            registros = listar_registros(db_id)
            for idx, reg in enumerate(registros, 1):
                print(f"\n======= Registro {idx} =======")
                for campo, valor in reg.items():
                    print(f"{campo}: {valor}")
        except Exception as e:
            print("Error al listar registros:", e)
    elif accion == "campos":
        try:
            campos = obtener_campos_base_datos(db_id)
            print("\nCampos de la base de datos:")
            for campo, tipo in campos.items():
                print(f"- {campo}: {tipo}")
        except Exception as e:
            print("Error al obtener campos:", e)
    else:
        print("Acción no reconocida.")
