'''Funciones auxiliares y datos fijos'''
from pathlib import Path
import psycopg2
import os

RAIZ = Path(__file__).resolve().parent.parent
CARPETA_CONSULTAS = RAIZ / "consultas"
ESCALAS = [1, 5, 10, 50, 1000]
RUTA_RESULTADOS = RAIZ / "resultados"
RUTA_CSV = RAIZ / "resultados" / "tiempos_crudos.csv"


def leer_consulta(ruta_sql):
    with open(ruta_sql, "r", encoding="utf-8") as archivo:
        return archivo.read()


def obtener_consultas():
    consultas = []
    for motor in CARPETA_CONSULTAS.iterdir():
        for clase in motor.iterdir():
            for consulta in clase.iterdir():
                if consulta.suffix != ".sql":  # por si acaso
                    continue
                datos = {
                    "motor": motor.name,
                    "clase": clase.name,
                    "nombre_consulta": consulta.stem,
                    "ruta": str(consulta.absolute()),
                    "sql": leer_consulta(consulta),
                }
                consultas.append(datos)
    return consultas


def conectar(nombre_base):
    return psycopg2.connect(
        host=os.environ.get("PGHOST"),
        port=os.environ.get("PGPORT"),
        dbname=nombre_base,
        user=os.environ.get("PGUSER"),
        password=os.environ.get("PGPASSWORD"),
    )
