'''Mide los tiempos'''
import time
from generador.cargar_oltp import conectar
from etl.equivalencia import conectar_duckdb, cargar_tablas_duckdb
import subprocess

def reiniciar_pg():
    # eajustar si es necesario
    subprocess.run(
        ["powershell", "-Command",
         "Restart-Service postgresql-x64-17"],
        check=True
    )
    time.sleep(2)

def medir_tiempo_postgres(conexion, sql, es_frio, nombre_base):
    if es_frio:
        if conexion:
            conexion.close()
        reiniciar_pg()
        conexion = conectar(nombre_base)

    inicio = time.perf_counter()
    with conexion.cursor() as cur:
        cur.execute(sql)
        cur.fetchall()  # importante: traer resultados para forzar la ejecución completa
    fin = time.perf_counter()

    return fin - inicio, conexion


def medir_tiempo_duckdb(sql, carpeta_olap, es_frio, conexion_existente=None):
    if es_frio:
        if conexion_existente:
            conexion_existente.close()

        conexion = conectar_duckdb()
        cargar_tablas_duckdb(conexion, carpeta_olap)
    else:
        conexion = conexion_existente

    inicio = time.perf_counter()
    conexion.execute(sql).fetchall()
    fin = time.perf_counter()

    return fin - inicio, conexion


def medir_una_consulta(item, escala, conexion_pg, carpeta_olap, conexion_duck, nombre_base):
    resultados = []

    # medición en frío (1 sola vez)
    if item["motor"] == "oltp":  # modificar conexion_pg
        tiempo, conexion_pg = medir_tiempo_postgres(
            conexion_pg, item["sql"], es_frio=True, nombre_base=nombre_base)
    else:  # modificar conexion_duck
        tiempo, conexion_duck = medir_tiempo_duckdb(
            item["sql"], carpeta_olap, es_frio=True, conexion_existente=conexion_duck)
       

    resultados.append({
        "escala": escala,
        "motor": item["motor"],
        "clase": item["clase"],
        "nombre_consulta": item["nombre_consulta"],
        "regimen": "frio",
        "repeticion": 0,
        "tiempo": tiempo
    })

    # mediciones en caliente (5 veces)
    for repeticion in range(1, 6):
        if item["motor"] == "oltp": # modificar conexion_pg
            tiempo, conexion_pg = medir_tiempo_postgres(
                conexion_pg, item["sql"], es_frio=False, nombre_base=nombre_base)
        else: # modificar conexion_duck
            tiempo, conexion_duck = medir_tiempo_duckdb(
                item["sql"], carpeta_olap, es_frio=False, conexion_existente=conexion_duck)

        resultados.append({
            "escala": escala,
            "motor": item["motor"],
            "clase": item["clase"],
            "nombre_consulta": item["nombre_consulta"],
            "regimen": "caliente",
            "repeticion": repeticion,
            "tiempo": tiempo
        })

    return resultados, conexion_pg, conexion_duck
