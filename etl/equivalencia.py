'''Inicializar los datos en duckdb y funciones verificadoras de equivalencia'''

import duckdb
from .utils import NOMBRE_DIMENSIONES, RAIZ
from generador.cargar_oltp import conectar


def conectar_duckdb():
    return duckdb.connect(database=":memory:")


def cargar_tablas_duckdb(con, carpeta_olap):
    for dimension in NOMBRE_DIMENSIONES:
        ruta = carpeta_olap / f"{dimension}.parquet"
        con.execute(f""" CREATE OR REPLACE TABLE {dimension} AS
                    SELECT *
                    FROM read_parquet('{ruta}')""")

    carpeta_fact = carpeta_olap / "hechos"

    con.execute(f"""
        CREATE OR REPLACE TABLE fact_reproducciones AS
        SELECT *
        FROM read_parquet('{carpeta_fact}/*.parquet')
    """)


def ejecutar_query_pg(conexion, query):

    cursor = conexion.cursor()

    cursor.execute(query)

    # selecciono el numero total de registros en vez de recibir todas las filas
    resultado = cursor.fetchone()[0]

    cursor.close()

    return resultado


def ejecutar_query_duck(conexion, query):

    resultado = conexion.execute(query).fetchone()[0]

    return resultado


def verificar(nombre, resultado_pg, resultado_duck):

    # son iguales asi q son equivalentes
    if resultado_pg == resultado_duck:
        print(f"{nombre}: PASA")
        return True

    # no son equivalentes (estas no funcionaran para la comparacion)
    else:
        print(
            f"{nombre}: FALLA "
            f"(PostgreSQL={resultado_pg}, DuckDB={resultado_duck})"
        )
        return False


def verificar_equivalencia(escala):

    nombre_base = f"db_streaming_escala{escala}"

    carpeta_olap = (
        RAIZ /
        "datos_olap" /
        f"escala_{escala}"
    )

    # conecto las bases
    conexion_pg = conectar(nombre_base)
    conexion_duck = conectar_duckdb()

    # con los archivos parquet ya generados, cargo los datos a la duckdb
    cargar_tablas_duckdb(
        conexion_duck,
        carpeta_olap
    )

    resultados = []

    # cantidad de reproducciones en postgres OLTP
    cantidad_reproducciones_pg = ejecutar_query_pg(
        conexion_pg,
        """
        SELECT COUNT(*)
        FROM reproducciones
        """
    )

    # cantidad de reproducciones en duckdb OLAP
    cantidad_reproducciones_duck = ejecutar_query_duck(
        conexion_duck,
        """
        SELECT COUNT(*)
        FROM fact_reproducciones
        """
    )

    # agrego a resultados la prueba de esta primera query
    resultados.append(
        verificar(
            "Filas reproducciones",
            cantidad_reproducciones_pg,
            cantidad_reproducciones_duck
        )
    )

    # para las dimensiones
    dimensiones = [
        (
            "usuarios",
            """
            SELECT COUNT(DISTINCT id_usuario)
            FROM usuarios
            """,
            """
            SELECT COUNT(*)
            FROM dim_usuario
            """
        ),

        (
            "artistas",
            """
            SELECT COUNT(DISTINCT id_artista)
            FROM artistas
            """,
            """
            SELECT COUNT(*)
            FROM dim_artista
            """
        ),

        (
            "canciones",
            """
            SELECT COUNT(DISTINCT id_cancion)
            FROM canciones
            """,
            """
            SELECT COUNT(*)
            FROM dim_cancion
            """
        )
    ]

    # por cada dimension probar la query
    for nombre, query_pg, query_duck in dimensiones:

        cantidad_pg = ejecutar_query_pg(
            conexion_pg,
            query_pg
        )

        cantidad_duck = ejecutar_query_duck(
            conexion_duck,
            query_duck
        )

        resultados.append(
            verificar(
                f"Entidades {nombre}",
                cantidad_pg,
                cantidad_duck
            )
        )

    # sumar metricas principales
    suma_tiempo_pg = ejecutar_query_pg(
        conexion_pg,
        """
        SELECT SUM(tiempo)
        FROM reproducciones
        """
    )

    suma_tiempo_duck = ejecutar_query_duck(
        conexion_duck,
        """
        SELECT SUM(tiempo)
        FROM fact_reproducciones
        """
    )

    resultados.append(
        verificar(
            "SUM tiempo escuchado",
            suma_tiempo_pg,
            suma_tiempo_duck
        )
    )

    conexion_pg.close()

    conexion_duck.close()

    print(f"Resulatados: {resultados}")
    # convierte la lista a un unico booleano, segun corresponda
    return all(resultados)
