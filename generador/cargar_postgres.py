import psycopg2
import os
import argparse
from dotenv import load_dotenv
from pathlib import Path
import time

load_dotenv()

CARPETA_ACTUAL = Path(__file__).parent
RAIZ_PROYECTO = CARPETA_ACTUAL.parent
RUTA_SCHEMA_OLTP = RAIZ_PROYECTO / "modelo" / "schema_oltp.sql"
# Orden de carga respetando las dependencias de FK
TABLAS = ["usuarios", "artistas", "generos", "canciones", "reproducciones"]

# Columnas de cada tabla, en el mismo orden que en los CSV que son los mismos del esquema
COLUMNAS = {
    "usuarios": ["id_usuario", "nombre", "email", "pais", "fecha_registro", "plan"],
    "artistas": ["id_artista", "nombre", "pais_origen", "genero_principal"],
    "generos": ["id_genero", "nombre"],
    "canciones": ["id_cancion", "duracion", "titulo", "id_artista", "id_genero"],
    "reproducciones": ["id_reproduccion", "id_usuario", "id_cancion", "tmsp", "dispositivo", "tiempo"],
}


# Conectar con las varibles de entorno para no hacerlo desde la terminal y poder inicializar postgres
def conectar(nombre_base):
    return psycopg2.connect(
        host=os.environ.get("PGHOST"),
        port=os.environ.get("PGPORT"),
        dbname=nombre_base,
        user=os.environ.get("PGUSER"),
        password=os.environ.get("PGPASSWORD"),
    )


def crear_base_si_no_existe(nombre_base):
    # se conecta a la base default para poder crear otras
    conn = conectar("postgres")
    conn.autocommit = True  # CREATE DATABASE no puede ir dentro de una transacción

    with conn.cursor() as cur:
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s",
                    (nombre_base,))
        existe = cur.fetchone() is not None

        if not existe:
            cur.execute(f"CREATE DATABASE {nombre_base}")
            print(f"Base de datos '{nombre_base}' creada.")
        else:
            print(f"Base de datos '{nombre_base}' ya existía.")

    conn.close()


def cargar_schema(nombre_base):
    conn = conectar(nombre_base)

    with open(RUTA_SCHEMA_OLTP, "r", encoding="utf-8") as archivo_sql:
        contenido_sql = archivo_sql.read()

    with conn.cursor() as cur:
        cur.execute(contenido_sql)

    conn.commit()
    conn.close()
    print(f"Schema OLTP cargado en '{nombre_base}'.")


def cargar_tabla(conn, nombre_tabla, ruta_csv):
    columnas = ", ".join(COLUMNAS[nombre_tabla])
    sql_copy = f"COPY {nombre_tabla}({columnas}) FROM STDIN WITH (FORMAT csv, HEADER true)"

    with conn.cursor() as cur:
        cur.execute(f"TRUNCATE TABLE {nombre_tabla} CASCADE")

        with open(ruta_csv, "r", encoding="utf-8") as archivo_csv:
            cur.copy_expert(sql_copy, archivo_csv)

    conn.commit()
    print(f"Tabla '{nombre_tabla}' cargada desde {ruta_csv}")


def main():
    parser = argparse.ArgumentParser(
        description="Crea la base de datos, carga el schema y los CSV para una escala dada")
    parser.add_argument("--s", type=int, required=True,
                        help="Factor de escala (debe coincidir con una carpeta ya generada)")
    args = parser.parse_args()

    nombre_base = f"db_streaming_escala{args.s}"
    carpeta_datos = RAIZ_PROYECTO / "datos" / "csv" / f"escala_{args.s}"

    crear_base_si_no_existe(nombre_base)
    cargar_schema(nombre_base)

    conn = conectar(nombre_base)
    try:
        for nombre_tabla in TABLAS:
            ruta_csv = carpeta_datos / f"{nombre_tabla}.csv"
            cargar_tabla(conn, nombre_tabla, ruta_csv)
    finally:
        conn.close()

    print(f"Carga completa para escala {args.s} en base '{nombre_base}'.")


if __name__ == "__main__":
    main()
