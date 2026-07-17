'''Funciones principales para exportar los datos OLTP a formato parquet'''

from pathlib import Path
import pandas as pd
from generador.config import TAMANO_CHUNK


def exportar_dimension(conexion, consulta_sql, carpeta_destino, nombre_dim):
    Path(carpeta_destino).mkdir(parents=True, exist_ok=True)

    df = pd.read_sql_query(consulta_sql, conexion)
    ruta_archivo = carpeta_destino / f"{nombre_dim}.parquet"

    df.to_parquet(ruta_archivo, index=False)


def exportar_fact(conexion, consulta_sql, carpeta_destino, nombre_fact, chunksize=TAMANO_CHUNK):
    Path(carpeta_destino).mkdir(parents=True, exist_ok=True)

    resultado = pd.read_sql_query(
        consulta_sql,
        conexion,
        chunksize=chunksize
    )

    for i, chunk in enumerate(resultado):
        ruta_archivo = carpeta_destino / f"{nombre_fact}_parte{i}.parquet"
        chunk.to_parquet(ruta_archivo, index=False)

    print(f"Tabla de hechos '{nombre_fact}' exportada en {carpeta_destino}")
