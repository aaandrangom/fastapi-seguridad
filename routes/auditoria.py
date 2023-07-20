from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from ConectionDB.conectionDB import bd
from routes.user import User, get_user_current

auditoria_routes = APIRouter()

class Auditoria(BaseModel):
    aud_id: Optional[int]
    aud_usuario: str
    aud_fecha: Optional[datetime]
    aud_accion: str
    aud_modulo: str
    aud_funcionalidad: str 
    aud_observacion: str


@auditoria_routes.get("/auditoria", tags=["Auditoria"])
async def get_auditoria(user: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        query = "SELECT * FROM tb_auditoria"
        cursor.execute(query)

        rows = cursor.fetchall()
        result = []
        columns = [column[0] for column in cursor.description]
        for row in rows:
            result.append(dict(zip(columns, row)))

        bd.CloseConection(conn)

        return {"tb_auditoria": result}
    except Exception as e:
        return {"message": "Error al obtener los datos de la tabla tb_auditoria", "error": str(e)}

@auditoria_routes.get("/auditoria/cerrar_sesion", tags=["Auditoria"])
async def get_auditoria(user: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()
        cursor.execute("EXEC sp_end_session")
        cursor.commit()
        return {"message": "Success Full: Session Cerrada en BD"}
    except Exception as e:
        return {"message": "Error al cerrar la session en BD"}
    
@auditoria_routes.post("/auditoria", tags=["Auditoria"])
async def create_auditoria(auditoria: Auditoria, user: User = Depends(get_user_current)):    
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        aud_usuario = auditoria.aud_usuario
        aud_fecha = datetime.now()
        aud_accion = auditoria.aud_accion
        aud_modulo = auditoria.aud_modulo
        aud_funcionalidad = auditoria.aud_funcionalidad
        aud_observacion = auditoria.aud_observacion

        query = "INSERT INTO tb_auditoria (aud_usuario, aud_fecha, aud_accion, aud_modulo, aud_funcionalidad, aud_observacion) VALUES (?, ?, ?, ?, ?, ?)"
        values = (aud_usuario, aud_fecha, aud_accion, aud_modulo, aud_funcionalidad, aud_observacion)
        cursor.execute(query, values)
        conn.commit()

        bd.CloseConection(conn)


        return {"message": "Datos insertados correctamente en la tabla tb_auditoria"}
    except Exception as e:
        return {"message": "Error al insertar datos en la tabla tb_auditoria", "error": str(e)}
    
@auditoria_routes.get("/auditoria/{aud_id}", tags=["Auditoria"])
async def get_auditoria(aud_id: int, user: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        query = "SELECT * FROM tb_auditoria WHERE aud_id = ?"
        cursor.execute(query, aud_id)
        row = cursor.fetchone()

        if row:
            aud_id = row[0]
            aud_usuario = row[1]
            aud_fecha = row[2]
            aud_accion  = row[3]
            aud_modulo = row[4]
            aud_funcionalidad = row[5]
            aud_observacion = row[6]

            bd.CloseConection(conn)

            return {
                "aud_id": aud_id,
                "aud_usuario": aud_usuario,
                "aud_fecha": aud_fecha,
                "aud_accion": aud_accion,
                "aud_modulo": aud_modulo,
                "aud_funcionalidad": aud_funcionalidad,
                "aud_observacion": aud_observacion
            }
        else:
            bd.CloseConection(conn)
            raise HTTPException(status_code=404, detail="Registro no encontrado")

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@auditoria_routes.delete("/auditoria/{aud_id}", tags=["Auditoria"])
async def delete_auditoria(aud_id: int, user: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        query = "DELETE FROM tb_auditoria WHERE aud_id = ?"
        cursor.execute(query, aud_id)
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
    
@auditoria_routes.put("/auditoria/{aud_id}", tags=["Auditoria"])
async def update_auditoria(aud_id: int, aud_usuario: str, aud_accion: str, aud_modulo: str, aud_funcionalidad: str, aud_observacion: str, user: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        query = "SELECT COUNT(*) FROM tb_auditoria WHERE aud_id = ?"
        cursor.execute(query, aud_id)
        row_count = cursor.fetchone()[0]

        if row_count == 0:
            bd.CloseConection(conn)
            raise HTTPException(status_code=404, detail="Registro no encontrado")

        query = "UPDATE tb_auditoria SET aud_usuario = ?, aud_accion = ?, aud_modulo = ?, aud_funcionalidad = ?,  aud_observacion = ? WHERE aud_id = ?"
        values = (aud_usuario, aud_accion, aud_modulo, aud_funcionalidad, aud_observacion, aud_id)
        cursor.execute(query, values)
        conn.commit()

        bd.CloseConection(conn)

        return {"message": "Registro actualizado correctamente"}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@auditoria_routes.get("/reporte-pista-auditoria/", tags=["Auditoria"])
async def get_auditoria(fecha_inicio: str, fecha_fin: str, user: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        query = '''
           SELECT
                a.aud_id AS "aud_id",
                u.usr_full_name AS "aud_usuario",
                FORMAT(a.aud_fecha, 'yyyy-MM-dd') AS "aud_fecha",
                a.aud_accion AS "aud_accion",
                m.mod_name AS "aud_modulo",
                a.aud_funcionalidad AS "aud_funcionalidad",
                a.aud_observacion AS "aud_observacion"
            FROM
                tb_auditoria a
            INNER JOIN
                tb_user u ON a.aud_usuario = u.usr_id
            INNER JOIN
                tb_module m ON a.aud_modulo = m.mod_name
            WHERE
                a.aud_fecha >= CONVERT(datetime, ?) AND
                a.aud_fecha < DATEADD(day, 1, CONVERT(datetime, ?))
            ORDER BY
                a.aud_fecha;

        '''

        cursor.execute(query, (fecha_inicio, fecha_fin))

        rows = cursor.fetchall()
        result = []
        columns = [column[0] for column in cursor.description]
        for row in rows:
            result.append(dict(zip(columns, row)))

        bd.CloseConection(conn)

        return {"tb_auditoria": result}
    except Exception as e:
        return {"message": "Error al obtener los datos de la tabla tb_auditoria", "error": str(e)}
