'''Funciones auxiliares y valores fijos'''

from pathlib import Path

NOMBRE_DIMENSIONES = [
    "dim_usuario",
    "dim_artista",
    "dim_cancion",
]
RAIZ = Path(__file__).resolve().parent.parent
CARPETA_CONSULTAS = RAIZ / "etl" / "consultas"


def leer_consulta(ruta_sql):
    with open(ruta_sql, "r", encoding="utf-8") as archivo:
        return archivo.read()
