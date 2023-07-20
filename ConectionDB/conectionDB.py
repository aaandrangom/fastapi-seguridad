import pyodbc
from math import e
class dbConection():

  server = "apdistserver.database.windows.net"  
  database = "SecurityDB"  

  def __init__(self, user, psw):
    # Configuración de la conexión a la base de datos
    self.user = user
    self.psw = psw

  def GetConectionString(self):
    # Cadena de conexión
    conn_str = (
      "DRIVER={ODBC Driver 17 for SQL Server};"
      f"SERVER={self.server},{1433};"
      f"DATABASE={self.database};"
      f"UID={self.user};"
      f"PWD={self.psw};"
    )
    return conn_str

  def OpenConection(self):
    try:
      conn = pyodbc.connect(self.GetConectionString())
      return conn
    except Exception as e:
      return {"ERROR FATAL": "ERROR AL CONECTAR LA BASE DE DATOS", "ERROR MESSAGE": str(e)}

  def CloseConection(self, conn):
    conn.close()

bd = dbConection("ajbenavidesp", "Paillacho10/10")
