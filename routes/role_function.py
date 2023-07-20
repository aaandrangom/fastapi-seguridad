from sys import int_info
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from ConectionDB.conectionDB import bd
from routes.user import User, get_user_current

role_function_routes = APIRouter()

class Role_function(BaseModel):
    rol_func_id: Optional[int]
    rol_func_role: int
    rol_func_function: int
    rol_func_state: str
    rol_func_date: Optional[datetime]


@role_function_routes.get("/role_function", tags=["Role-Function"])
async def get_role_function(user: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        query = "SELECT * FROM tb_role_function"
        cursor.execute(query)

        rows = cursor.fetchall()
        result = []
        columns = [column[0] for column in cursor.description]
        for row in rows:
            result.append(dict(zip(columns, row)))

        bd.CloseConection(conn)

        return {"tb_role_function": result}
    except Exception as e:
        return {"message": "Error al obtener los datos de la tabla tb_role_function", "error": str(e)}
    
@role_function_routes.post("/role_function", tags=["Role-Function"])
async def create_role_function(role_function: Role_function, user: User = Depends(get_user_current)):    
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        rol_func_role = role_function.rol_func_role
        rol_func_function = role_function.rol_func_function
        rol_func_state = role_function.rol_func_state
        rol_func_date = datetime.now()

        query = "INSERT INTO tb_role_function (rol_func_role, rol_func_function, rol_func_state, rol_func_date) VALUES (?, ?, ?, ?)"
        values = (rol_func_role, rol_func_function, rol_func_state, rol_func_date)
        cursor.execute(query, values)
        conn.commit()

        bd.CloseConection(conn)


        return {"message": "Datos insertados correctamente en la tabla tb_role_function"}
    except Exception as e:
        return {"message": "Error al insertar datos en la tabla tb_role_function", "error": str(e)}
    
@role_function_routes.get("/role_function/{rol_func_id}", tags=["Role-Function"])
async def get_role_function(rol_func_id: int, user: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        query = "SELECT * FROM tb_role_function WHERE rol_func_id = ?"
        cursor.execute(query, rol_func_id)
        row = cursor.fetchone()

        if row:
            rol_func_id = row[0]
            rol_func_role = row[1]
            rol_func_function = row[2]
            rol_func_state  = row[3]
            rol_func_date = row[4]

            bd.CloseConection(conn)

            return {
                "rol_func_id": rol_func_id,
                "rol_func_role": rol_func_role,
                "rol_func_function": rol_func_function,
                "rol_func_state": rol_func_state,
                "rol_func_date": rol_func_date
            }
        else:
            bd.CloseConection(conn)
            raise HTTPException(status_code=404, detail="Registro no encontrado")

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@role_function_routes.get("/role_function/role/{rol_func_role}", tags=["Role-Function"])
async def get_role_function(rol_func_role: int, user: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        query = "SELECT * FROM tb_role_function WHERE rol_func_role = ?"
        cursor.execute(query, rol_func_role)
        rows = cursor.fetchall()
        result = []
        columns = [column[0] for column in cursor.description]
        for row in rows:
            result.append(dict(zip(columns, row)))
        bd.CloseConection(conn)
        return {"tb_role_function": result}
    except Exception as e:
        return {"message": "Error al obtener los datos de la tabla tb_role_function por role", "error": str(e)}
    
@role_function_routes.delete("/role_function/{rol_func_id}", tags=["Role-Function"])
async def delete_role_function(rol_func_id: int, user: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        query = "DELETE FROM tb_role_function WHERE rol_func_id = ?"
        cursor.execute(query, rol_func_id)
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
    
@role_function_routes.put("/role_function/{rol_func_id}", tags=["Role-Function"])
async def update_role_function(rol_func_id: int, rol_func_role: int, rol_func_function: int, rol_func_state: str, user: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        query = "SELECT COUNT(*) FROM tb_role_function WHERE rol_func_id = ?"
        cursor.execute(query, rol_func_id)
        row_count = cursor.fetchone()[0]

        if row_count == 0:
            bd.CloseConection(conn)
            raise HTTPException(status_code=404, detail="Registro no encontrado")

        query = "UPDATE tb_role_function SET rol_func_role = ?, rol_func_function = ?, rol_func_state = ? WHERE rol_func_id = ?"
        values = (rol_func_role, rol_func_function, rol_func_state, rol_func_id)
        cursor.execute(query, values)
        conn.commit()

        bd.CloseConection(conn)

        return {"message": "Registro actualizado correctamente"}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))