{
  "openapi": "3.0.0",
  "info": {
    "title": "Agente Notion",
    "version": "1.0.0",
    "description": "Asistente para integrar ChatGPT con Notion: consulta y actualiza tareas en bases de datos relacionadas con obras, contratistas y pagos."
  },
  "servers": [
    {
      "url": "https://notion-gpt-agent.onrender.com"
    }
  ],
  "paths": {
    "/": {
      "get": {
        "summary": "Verifica que la API esté funcionando",
        "responses": {
          "200": {
            "description": "API funcionando correctamente"
          }
        }
      }
    }
  }
}
