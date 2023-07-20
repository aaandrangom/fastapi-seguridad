from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from ConectionDB.conectionDB import bd
from routes.user import User, get_user_current

role_routes = APIRouter()

class Role(BaseModel):
    rol_id: Optional[int]
    rol_role: str
    rol_description: str
    rol_allowed_users: int
    rol_state : str 
    rol_date: Optional[datetime]


@role_routes.get("/role", tags=["Role"])
async def get_role(user: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        query = "SELECT * FROM tb_role"
        cursor.execute(query)

        rows = cursor.fetchall()
        result = []
        columns = [column[0] for column in cursor.description]
        for row in rows:
            result.append(dict(zip(columns, row)))

        bd.CloseConection(conn)


        return {"role": result}
    except Exception as e:
        return {"message": "Error al obtener los datos de la tabla tb_role", "error": str(e)}

@role_routes.get("/role/{rol_id}", tags=["Role"])
async def get_role(rol_id: int, user: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        query = "select * from tb_role where rol_id = ?"
        cursor.execute(query, rol_id)
        row = cursor.fetchone()

        if row:
            rol_id = row[0]
            rol_role = row[1]
            rol_description = row[2]
            rol_allowed_users = row[3]
            rol_state = row[4]
            rol_date = row[5]
            
            bd.CloseConection(conn)


            return{
                "rol_id": rol_id,
                "rol_role": rol_role,
                "rol_description": rol_description,
                "rol_allowed_users": rol_allowed_users,
                "rol_state": rol_state,
                "rol_date": rol_date
            }
        else:
            bd.CloseConection(conn)

            
            raise HTTPException(status_code=404, detail="Registro no encontrado")
    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@role_routes.post("/role", tags=["Role"])
async def create_role(role: Role, user: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        rol_role = role.rol_role
        rol_description = role.rol_description
        rol_allowed_users = role.rol_allowed_users
        rol_state = role.rol_state
        rol_date = datetime.now()

        query = "insert into tb_role (rol_role, rol_description, rol_allowed_users, rol_state, rol_date)  VALUES (?, ?, ?, ?, ?)"
        values =(rol_role, rol_description, rol_allowed_users, rol_state, rol_date)
        
        cursor.execute(query, values)
        conn.commit()

        bd.CloseConection(conn)

        return {"message": "Datos insertados correctamente en la tabla tb_role"}
    except Exception as e:
        return {"message": "Error al insertar datos en la tabla Role", "error": str(e)}

@role_routes.delete("/role/{rol_id}", tags=["Role"])
async def delete_role(rol_id: int, user: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        query = "DELETE FROM tb_role WHERE rol_id = ?"
        cursor.execute(query, rol_id)
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

@role_routes.put("/role/{rol_id}", tags=["Role"])
async def update_role(rol_id: int, rol_role: str, rol_description: str, rol_allowed_users: int, rol_state: str, user: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        query = "SELECT COUNT(*) FROM tb_role WHERE rol_id = ?"
        cursor.execute(query, rol_id)
        row_count = cursor.fetchone()[0]

        if row_count == 0:
            bd.CloseConection(conn)


            raise HTTPException(status_code=404, detail="Registro no encontrado")

        query = "UPDATE tb_role SET rol_role = ?, rol_description = ?, rol_allowed_users = ?, rol_state = ? WHERE rol_id = ?"
        values = (rol_role, rol_description, rol_allowed_users, rol_state, rol_id)
        cursor.execute(query, values)
        conn.commit()

        bd.CloseConection(conn)


        return {"message": "Registro actualizado correctamente"}

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
