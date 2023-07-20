from math import e
from fastapi import FastAPI
from routes.role_user import role_user_routes
from routes.role import role_routes
from routes.user import user_routes, token_routes
from routes.module import module_routes
from routes.functions import function_routes
from routes.role_function import role_function_routes 
from routes.auditoria import auditoria_routes
from ConectionDB.conectionDB import bd

app = FastAPI()

@app.get("/")
async def index():
    try:
        conn = bd.OpenConection()
        conn.execute("select * from tb_user")
        return "Conexión exitosa a la base de datos."
    except Exception as e:
        return f"Error al conectarse a la base de datos: {e}"



app.include_router(user_routes, prefix="/api")
app.include_router(role_user_routes, prefix="/api")
app.include_router(role_routes, prefix="/api")
app.include_router(module_routes, prefix="/api")
app.include_router(function_routes, prefix="/api")
app.include_router(role_function_routes, prefix="/api")
app.include_router(auditoria_routes, prefix="/api")
app.include_router(token_routes)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)

