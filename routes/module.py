from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from ConectionDB.conectionDB import bd
from routes.user import User, get_user_current

module_routes = APIRouter()

class Module(BaseModel):
    mod_id: Optional[int]
    mod_name: str
    mod_admin: str
    mod_state: str
    mod_date: Optional[datetime]


@module_routes.get("/module", tags=["Module"])
async def get_module(user: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        query = "SELECT * FROM tb_module"
        cursor.execute(query)

        rows = cursor.fetchall()
        result = []
        columns = [column[0] for column in cursor.description]
        for row in rows:
            result.append(dict(zip(columns, row)))

        bd.CloseConection(conn)

        return {"tb_module": result}
    except Exception as e:
        return {"message": "Error al obtener los datos de la tabla tb_module", "error": str(e)}
    
@module_routes.post("/module", tags=["Module"])
async def create_module(module: Module, user: User = Depends(get_user_current)):    
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        mod_name = module.mod_name
        mod_admin = module.mod_admin
        mod_state = module.mod_state
        mod_date = datetime.now()

        query = "INSERT INTO tb_module (mod_name, mod_admin, mod_state, mod_date) VALUES (?, ?, ?, ?)"
        values = (mod_name, mod_admin, mod_state, mod_date)
        cursor.execute(query, values)
        conn.commit()

        bd.CloseConection(conn)


        return {"message": "Datos insertados correctamente en la tabla tb_module"}
    except Exception as e:
        return {"message": "Error al insertar datos en la tabla tb_module", "error": str(e)}
    
@module_routes.get("/module/{mod_id}", tags=["Module"])
async def get_module(mod_id: int, user: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        query = "SELECT * FROM tb_module WHERE mod_id = ?"
        cursor.execute(query, mod_id)
        row = cursor.fetchone()

        if row:
            mod_id = row[0]
            mod_name = row[1]
            mod_admin = row[2]
            mod_state  = row[3]
            mod_date = row[4]

            bd.CloseConection(conn)

            return {
                "mod_id": mod_id,
                "mod_name": mod_name,
                "mod_admin": mod_admin,
                "mod_state": mod_state,
                "mod_date": mod_date
            }
        else:
            bd.CloseConection(conn)
            raise HTTPException(status_code=404, detail="Registro no encontrado")

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@module_routes.delete("/module/{mod_id}", tags=["Module"])
async def delete_module(mod_id: int, user: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        query = "DELETE FROM tb_module WHERE mod_id = ?"
        cursor.execute(query, mod_id)
        conn.commit()

        if cursor.rowcount > 0:
            bd.CloseConection(conn)
            return {"message": "Registro eliminado correctamente"}
        else:
            bd.CloseConection(conn)
            raise HTTPException(status_code=404, detail="Registro no encontrado")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@module_routes.put("/module/{mod_id}", tags=["Module"])
async def update_module(mod_id: int, mod_name: str, mod_admin: str, mod_state: str, user: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        query = "SELECT COUNT(*) FROM tb_module WHERE mod_id = ?"
        cursor.execute(query, mod_id)
        row_count = cursor.fetchone()[0]

        if row_count == 0:
            bd.CloseConection(conn)
            raise HTTPException(status_code=404, detail="Registro no encontrado")

        query = "UPDATE tb_module SET mod_name = ?, mod_admin = ?, mod_state = ? WHERE mod_id = ?"
        values = (mod_name, mod_admin, mod_state, mod_id)
        cursor.execute(query, values)
        conn.commit()

        bd.CloseConection(conn)

        return {"message": "Registro actualizado correctamente"}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))