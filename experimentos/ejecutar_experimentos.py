'''Main de ejecucion'''

from .medir import medir_una_consulta
from .utils import obtener_consultas, RAIZ, ESCALAS, RUTA_RESULTADOS, conectar
from etl.equivalencia import conectar_duckdb, cargar_tablas_duckdb
import argparse
import pandas as pd

def correr_experimento_para_escala(escala):
    nombre_base = f"db_streaming_escala{escala}"
    carpeta_olap = RAIZ / "datos_olap" / f"escala_{escala}"
    conexion_pg = conectar(nombre_base)
    conexion_dk = conectar_duckdb()
    cargar_tablas_duckdb(conexion_dk, carpeta_olap)

    resultado_escalas = []
    consultas = obtener_consultas()
    for consulta in consultas:
        resultados, conexion_pg, conexion_dk = medir_una_consulta(consulta, escala, conexion_pg, carpeta_olap, conexion_dk, nombre_base)
        resultado_escalas.extend(resultados)
    conexion_pg.close()
    conexion_dk.close()
    return resultado_escalas

def correr_experimento_completo():
    # (recorre las 5 escalas fijas)
    resultados = []
    for escala in ESCALAS:
        print(f"Experimento en escala {escala}")
        resultado = correr_experimento_para_escala(escala) # devuelve un dict
        resultados.extend(resultado) # lo agrega valor por valor
    df = pd.DataFrame(resultados)
    return df 


def main():
    parser = argparse.ArgumentParser(description="Corre los experimentos de medición OLTP vs OLAP")
    parser.add_argument("--s", type=int, required=False, default=None,
                        help="Escala específica a correr (opcional). Si no se especifica, corre las 5 escalas completas.")
    args = parser.parse_args()
    # recibe una escala opcional para probar

    if args.s is not None:
        resultados = correr_experimento_para_escala(args.s) # si se le paso una escala corre esa 
        df = pd.DataFrame(resultados)
    else:
        df = correr_experimento_completo()

    # guardar df a CSV, etc.
    RUTA_RESULTADOS.mkdir(parents=True, exist_ok=True)

    ruta_archivo = RUTA_RESULTADOS / "tiempos_crudos.csv"
    df.to_csv(ruta_archivo, index=False)

    print(f"Resultados guardados en {ruta_archivo}")


if __name__ == "__main__":
    main()
