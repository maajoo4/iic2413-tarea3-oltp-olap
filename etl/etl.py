'''Main para la transformacion OLTP a parquet'''

from generador.cargar_oltp import conectar
import time
from .exportar import exportar_dimension, exportar_fact
from .utils import leer_consulta, RAIZ, CARPETA_CONSULTAS
import argparse


def ejecutar_etl(escala):

    carpeta_destino = RAIZ / "datos_olap" / f"escala_{escala}"
    nombre_base = f"db_streaming_escala{escala}"
    inicio = time.perf_counter()
    conexion = conectar(nombre_base)
    print(f"Conectar a la base: {time.perf_counter() - inicio:.2f} s")
    try:
        # Dimensiones
        dimensiones = [
            "dim_artista",
            "dim_cancion",
            "dim_usuario",
        ]

        for dimension in dimensiones:
            inicio = time.perf_counter()
            consulta = leer_consulta(
                CARPETA_CONSULTAS / f"{dimension}.sql")

            exportar_dimension(
                conexion,
                consulta,
                carpeta_destino,
                dimension,
            )
            print(
                f"Exportar {dimension}: {time.perf_counter() - inicio:.2f} s")

        # Tabla de hechos
        inicio = time.perf_counter()
        consulta = leer_consulta(CARPETA_CONSULTAS / "fact_reproducciones.sql")

        exportar_fact(
            conexion,
            consulta,
            carpeta_destino / "hechos",
            "reproducciones",
        )
        print(f"Exportar fact: {time.perf_counter() - inicio:.2f} s")

    finally:
        conexion.close()

    print(f"ETL de la escala {escala} completado correctamente.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--s", type=int, required=True)
    args = parser.parse_args()
    inicio_total = time.perf_counter()
    ejecutar_etl(args.s)
    print(f"Tiempo total ETL: {time.perf_counter() - inicio_total:.2f} s")


if __name__ == "__main__":
    main()
