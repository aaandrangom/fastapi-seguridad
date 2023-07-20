from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from ConectionDB.conectionDB import bd
from routes.user import User, get_user_current

function_routes = APIRouter()

class Function(BaseModel):
    func_id: Optional[int]
    func_name: str
    func_module: int
    func_state: str
    func_date: Optional[datetime]


@function_routes.get("/function", tags=["Function"])
async def get_function(user: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        query = "SELECT * FROM tb_function"
        cursor.execute(query)

        rows = cursor.fetchall()
        result = []
        columns = [column[0] for column in cursor.description]
        for row in rows:
            result.append(dict(zip(columns, row)))

        bd.CloseConection(conn)

        return {"tb_function": result}
    except Exception as e:
        return {"message": "Error al obtener los datos de la tabla tb_function", "error": str(e)}
    
@function_routes.post("/function", tags=["Function"])
async def create_function(function: Function, user: User = Depends(get_user_current)):    
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        func_name = function.func_name
        func_module = function.func_module
        func_state = function.func_state
        func_date = datetime.now()

        query = "INSERT INTO tb_function (func_name, func_module, func_state, func_date) VALUES (?, ?, ?, ?)"
        values = (func_name, func_module, func_state, func_date)
        cursor.execute(query, values)
        conn.commit()

        bd.CloseConection(conn)


        return {"message": "Datos insertados correctamente en la tabla tb_function"}
    except Exception as e:
        return {"message": "Error al insertar datos en la tabla tb_function", "error": str(e)}

@function_routes.get("/function_mod/{mod_id}", tags=["Function"])
async def get_function(mod_id: int, user: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        query = "SELECT * FROM tb_function WHERE func_module = ?"
        cursor.execute(query, mod_id)
        rows = cursor.fetchall()
        result = []
        columns = [column[0] for column in cursor.description]
        for row in rows:
            result.append(dict(zip(columns, row)))

        bd.CloseConection(conn)

        return {"tb_function": result}
    except Exception as e:
        return {"message": f"Error al obtener las funciones del modulo {mod_id}", "error": str(e)}

@function_routes.get("/function/{func_id}", tags=["Function"])
async def get_function(func_id: int, user: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        query = "SELECT * FROM tb_function WHERE func_id = ?"
        cursor.execute(query, func_id)
        row = cursor.fetchone()

        if row:
            func_id = row[0]
            func_name = row[1]
            func_module = row[2]
            func_state  = row[3]
            func_date = row[4]

            bd.CloseConection(conn)

            return {
                "func_id": func_id,
                "func_name": func_name,
                "func_module": func_module,
                "func_state": func_state,
                "func_date": func_date
            }
        else:
            bd.CloseConection(conn)
            raise HTTPException(status_code=404, detail="Registro no encontrado")

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@function_routes.delete("/function/{func_id}", tags=["Function"])
async def delete_function(func_id: int, user: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        query = "DELETE FROM tb_function WHERE func_id = ?"
        cursor.execute(query, func_id)
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
    
@function_routes.put("/function/{func_id}", tags=["Function"])
async def update_function(func_id: int, func_name: str, func_module: int, func_state: str, user: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        query = "SELECT COUNT(*) FROM tb_function WHERE func_id = ?"
        cursor.execute(query, func_id)
        row_count = cursor.fetchone()[0]

        if row_count == 0:
            bd.CloseConection(conn)
            raise HTTPException(status_code=404, detail="Registro no encontrado")

        query = "UPDATE tb_function SET func_name = ?, func_module = ?, func_state = ? WHERE func_id = ?"
        values = (func_name, func_module, func_state, func_id)
        cursor.execute(query, values)
        conn.commit()

        bd.CloseConection(conn)

        return {"message": "Registro actualizado correctamente"}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))