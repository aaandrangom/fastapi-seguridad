from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from ConectionDB.conectionDB import bd
from routes.user import User, get_user_current

role_user_routes = APIRouter()

# Role_user
class Role_user(BaseModel):
    rol_usr_id: Optional[int]
    rol_usr_user: str
    rol_usr_role: int
    rol_usr_state: str
    rol_usr_date: Optional[datetime]

@role_user_routes.get("/role_user", tags=["Role-user"])
async def get_role_user(user: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        query = "SELECT * FROM tb_role_user"
        cursor.execute(query)

        rows = cursor.fetchall()
        result = []
        columns = [column[0] for column in cursor.description]
        for row in rows:
            result.append(dict(zip(columns, row)))

        bd.CloseConection(conn)

        return {"tb_role_user": result}
    except Exception as e:
        return {"message": "Error al obtener los datos de la tabla tb_role_user", "error": str(e)}

@role_user_routes.post("/role_user", tags=["Role-user"])
async def create_role_user(role_user: Role_user, user: User = Depends(get_user_current)):
    try:
        # Establecer la conexión a la base de datos
        conn = bd.OpenConection()
        cursor = conn.cursor()

        rol_usr_user = role_user.rol_usr_user
        rol_usr_role = role_user.rol_usr_role
        rol_usr_state = role_user.rol_usr_state
        rol_usr_date = datetime.now()

        query = "INSERT INTO tb_role_user (rol_usr_user, rol_usr_role, rol_usr_state, rol_usr_date) VALUES (?, ?, ?, ?)"
        values = (rol_usr_user, rol_usr_role, rol_usr_state, rol_usr_date)
        cursor.execute(query, values)
        conn.commit()

        bd.CloseConection(conn)


        return {"message": "Datos insertados correctamente en la tabla tb_role_user"}
    except Exception as e:
        return {"message": "Error al insertar datos en la tabla tb_role_user", "error": str(e)}

@role_user_routes.get("/role_user/{rol_usr_id}", tags=["Role-user"])
async def get_role_user(rol_usr_id: int, user: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        query = "SELECT * FROM tb_role_user WHERE rol_usr_id = ?"
        cursor.execute(query, rol_usr_id)
        row = cursor.fetchone()

        if row:
            # Obtener los valores de las columnas
            rol_usr_id = row[0]
            rol_usr_user = row[1]
            rol_usr_role = row[2]
            rol_usr_state  = row[3]
            rol_usr_date = row[4]

            bd.CloseConection(conn)


            return {
                "rol_usr_id": rol_usr_id,
                "rol_usr_user": rol_usr_user,
                "rol_usr_role": rol_usr_role,
                "rol_usr_state": rol_usr_state,
                "rol_usr_date": rol_usr_date
            }
        else:
            bd.CloseConection(conn)
            raise HTTPException(status_code=404, detail="Registro no encontrado")

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@role_user_routes.delete("/role_user/{rol_usr_id}", tags=["Role-user"])
async def delete_role_user(rol_usr_id: int, user: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        query = "DELETE FROM tb_role_user WHERE rol_usr_id = ?"
        cursor.execute(query, rol_usr_id)
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
    
@role_user_routes.put("/role_user/{rol_usr_id}", tags=["Role-user"])
async def update_role_user(rol_usr_id: int, rol_usr_user: str, rol_usr_role: int, rol_usr_state: str, user: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        query = "SELECT COUNT(*) FROM tb_role_user WHERE rol_usr_id = ?"
        cursor.execute(query, rol_usr_id)
        row_count = cursor.fetchone()[0]

        if row_count == 0:
            bd.CloseConection(conn)
            raise HTTPException(status_code=404, detail="Registro no encontrado")

        query = "UPDATE tb_role_user SET rol_usr_user = ?, rol_usr_role = ?, rol_usr_state = ? WHERE rol_usr_id = ?"
        values = (rol_usr_user, rol_usr_role, rol_usr_state, rol_usr_id )
        cursor.execute(query, values)
        conn.commit()

        bd.CloseConection(conn)

        return {"message": "Registro actualizado correctamente"}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@role_user_routes.get("/role_user/user/{rol_usr_user}", tags=["Role-user"])
async def get_role_user_user(rol_usr_user: str, user: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        query = "SELECT * FROM tb_role_user WHERE rol_usr_user = ?"
        cursor.execute(query, rol_usr_user)
        rows = cursor.fetchall()
        result = []  
        if rows:
            columns = [column[0] for column in cursor.description]
            for row in rows:
                result.append(dict(zip(columns, row)))
            bd.CloseConection(conn)
            return {"tb_role_user_user": result}
        else:
            bd.CloseConection(conn)
            raise HTTPException(status_code=404, detail=f"Registros del usuario {rol_usr_user} no encontrados")      
    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))