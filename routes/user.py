from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from ConectionDB.conectionDB import bd
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Union
from jose import jwt, JWTError

user_routes = APIRouter()

token_routes = APIRouter()
oauth2_scheme = OAuth2PasswordBearer("/token")

SECRET_KEY = "b1664565cdeb4f67e77ab0cafcb64d09b729639ae2c7e9c9ba315f956de78473"
ALGORITHM = "HS256"

class User(BaseModel):
    usr_id: str
    usr_first_name: str
    usr_second_name: str
    usr_first_lastname: str
    usr_second_lastname : str
    usr_full_name: Optional[str]
    usr_user: str    
    usr_email: EmailStr
    usr_password: str
    usr_state: Optional[str]
    usr_date: Optional[datetime]

#Validacion del usuario con el token
async def get_user_current(token: str = Depends(oauth2_scheme)):
    try:
        token_decode = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        cedula = token_decode.get("sub")
        if cedula == None:
            raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})        
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    user = await get_user(cedula)
    if not user:
        raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    return user

async def get_user_disabled_current(user: User = Depends(get_user_current)):
    print("state", user.usr_state)
    if user.usr_state != "A":
       raise HTTPException(status_code=400, detail="The user is deactivated")
    return user


#CRUD USER
@user_routes.get("/user", tags=["User"])
async def get_user(user: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        query = "select * from tb_user"
        cursor.execute(query)

        rows = cursor.fetchall()
        result = []
        columns = [column[0] for column in cursor.description]
        for row in rows:
            result.append(dict(zip(columns, row)))

        bd.CloseConection(conn)


        return {"tb_user": result}
    except Exception as e:
        return {"message": "Error al obtener los datos de la tabla tb_user",  "error": str(e)}

@user_routes.get("/user/{usr_id}", tags=["User"])
async def get_user_by_cedula(usr_id: str, user: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        query = "select * from tb_user where usr_id = ?"
        cursor.execute(query, usr_id)
        row = cursor.fetchone()

        if row:
            usr_id = row[0]
            usr_first_name = row[1]
            usr_second_name = row[2]
            usr_first_lastname = row[3]
            usr_second_lastname = row[4]
            usr_full_name = row[5]
            usr_user  = row[6]     
            usr_email = row[7]
            usr_password = row[8]
            usr_state = row[9]
            usr_date = row[10]
            
            bd.CloseConection(conn)


            return{
                "usr_id": usr_id,
                "usr_first_name": usr_first_name,
                "usr_second_name": usr_second_name,
                "usr_first_lastname": usr_first_lastname,
                "usr_second_lastname": usr_second_lastname,
                "usr_full_name": usr_full_name,
                "usr_user": usr_user,
                "usr_email": usr_email,
                "usr_password": usr_password,
                "usr_state": usr_state,
                "usr_date": usr_date,
            }
        else:            
            bd.CloseConection(conn)

            
            raise HTTPException(status_code=404, detail="Registro no encontrado")
    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@user_routes.get("/user_email/{usr_email}", tags=["User"])
async def get_user_by_email(usr_email: str, user: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        query = "select * from tb_user where usr_email = ?"
        cursor.execute(query, usr_email)
        row = cursor.fetchone()

        if row:
            usr_id = row[0]
            usr_first_name = row[1]
            usr_second_name = row[2]
            usr_first_lastname = row[3]
            usr_second_lastname = row[4]
            usr_full_name = row[5]
            usr_user  = row[6]     
            usr_email = row[7]
            usr_password = row[8]
            usr_state = row[9]
            usr_date = row[10]
            
            bd.CloseConection(conn)


            return{
                "usr_id": usr_id,
                "usr_first_name": usr_first_name,
                "usr_second_name": usr_second_name,
                "usr_first_lastname": usr_first_lastname,
                "usr_second_lastname": usr_second_lastname,
                "usr_full_name": usr_full_name,
                "usr_user": usr_user,
                "usr_email": usr_email,
                "usr_password": usr_password,
                "usr_state": usr_state,
                "usr_date": usr_date,
            }
        else:            
            bd.CloseConection(conn)

            
            raise HTTPException(status_code=404, detail="Registro no encontrado")
    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_routes.get("/login", tags=["User"])
async def get_user_login(user_username: str, user_password: str, mod_name: str, user: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        query = "SELECT f.func_name FROM tb_user u JOIN tb_role_user ru ON u.usr_id = ru.rol_usr_user JOIN tb_role_function rf ON ru.rol_usr_role = rf.rol_func_role JOIN tb_function f ON rf.rol_func_function = f.func_id JOIN tb_module m ON f.func_module = m.mod_id WHERE u.usr_user = ? AND u.usr_password = ? AND m.mod_name = ?"
        cursor.execute(query, (user_username, user_password,mod_name))
        rows = cursor.fetchall()

        result=[]
        for index, row in enumerate(rows, start=1):
            result.append({str(index): row[0]})

        cursor.execute("EXEC sp_start_session @usr_user=?", user_username)
        cursor.commit()
        return result    
    except Exception as e:
        return {"error" : "Error al inciar Sesion"}    

 
@user_routes.post("/user", tags=["User"])
async def create_user(user: User, userAuthenticate: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        usr_id = user.usr_id
        usr_first_name = user.usr_first_name
        usr_second_name = user.usr_second_name
        usr_first_lastname = user.usr_first_lastname
        usr_second_lastname = user.usr_second_lastname
        usr_full_name = f"{usr_first_name} {usr_second_name} {usr_first_lastname} {usr_second_lastname}" 
        usr_user  = user.usr_user   
        usr_email = user.usr_email
        usr_password = user.usr_password
        usr_state = "A"
        usr_date = datetime.now()

        query = "insert into tb_user (usr_id, usr_first_name, usr_second_name, usr_first_lastname, usr_second_lastname, usr_full_name, usr_user, usr_email, usr_password, usr_state, usr_date)  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        values =(usr_id, usr_first_name, usr_second_name, usr_first_lastname,
                 usr_second_lastname, usr_full_name, usr_user, usr_email,
                 usr_password, usr_state, usr_date)
        
        cursor.execute(query, values)
        conn.commit()

        bd.CloseConection(conn)

        return {"message": "Datos insertados correctamente en la tabla tb_user"}
    except Exception as e:
        return {"message": "Error al insertar datos en la tabla tb_user", "error": str(e)}
        
@user_routes.put("/user/{usr_id}", tags=["User"])
async def update_user(usr_id: str, usr_id_update: str, usr_first_name: str,
                    usr_second_name: str, usr_first_lastname : str, usr_second_lastname: str,
                    usr_user: str, usr_email: str, usr_password: str, usr_state: str, user: User = Depends(get_user_current)):
    
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        query = "SELECT COUNT(*) FROM tb_user WHERE usr_id = ?"
        cursor.execute(query, usr_id)
        row_count = cursor.fetchone()[0]

        if row_count == 0:
            bd.CloseConection(conn)


            raise HTTPException(status_code=404, detail="Registro no encontrado")

        query = '''
            update tb_user set usr_id = ?, usr_first_name = ?, 
            usr_second_name = ?, usr_first_lastname = ?, usr_second_lastname = ?,
            usr_full_name = ?, usr_user = ?, usr_email  = ?, usr_password =?, 
            usr_state = ? Where usr_id = ?
        '''

        usr_full_name = f"{usr_first_name} {usr_second_name} {usr_first_lastname} {usr_second_lastname}"

        values = (usr_id_update, usr_first_name, usr_second_name, usr_first_lastname, usr_second_lastname,
                 usr_full_name, usr_user, usr_email, usr_password, usr_state, usr_id)
        
        cursor.execute(query, values)
        conn.commit()

        bd.CloseConection(conn)


        return {"message": "Registro actualizado correctamente"}

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@user_routes.delete("/user/{usr_id}", tags=["User"])
async def delete_user(usr_id: str, user: User = Depends(get_user_current)):
    try:
        conn = bd.OpenConection()
        cursor = conn.cursor()

        query = "DELETE FROM tb_user WHERE usr_id = ?"
        cursor.execute(query, usr_id)
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
    
#Complementacion

async def get_user(cedula):
    user_data = await get_user_by_cedula(cedula)
    return User(**user_data)

def verify_password(form_password, db_password):
    if form_password == db_password:
        return True
    else:
        return False

async def authenticate_user(cedula, password):
    user = await get_user(cedula)
    if not user:
        raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    if not verify_password(password, user.usr_password):
        raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    return user

def create_token(data: dict, time_expire: Union[datetime, None] = None):
    data_copy = data.copy()
    if time_expire is None:
        expire = datetime.utcnow() + timedelta(days=60)
    else:
        expire = datetime.utcnow() + time_expire
    data_copy.update({"exp": expire})
    token_jwt = jwt.encode(data_copy, key=SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt

@token_routes.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    access_token_expires = timedelta(days=60)
    access_token_jwt = create_token({"sub": user.usr_id}, access_token_expires)
    return {
        "access_token": access_token_jwt,
        "token_type": "bearer"
    }

@token_routes.get("/user/me", tags=["User"])
def user(user: User = Depends(get_user_current)):
    return user

#####################