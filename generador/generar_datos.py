import argparse
import random
import numpy as np
from faker import Faker
import time  # ver tiempos

from .config import (
    BASE_USUARIOS,
    BASE_ARTISTAS,
    BASE_CANCIONES,
    BASE_REPRODUCCIONES,
    SEMILLA,
    TAMANO_CHUNK,
    RAIZ_PROYECTO
)
from .generadores import (
    generar_usuarios,
    generar_artistas,
    generar_generos,
    generar_canciones
)
from .exportar_datos import guardar_csv, guardar_reproducciones_csv


def main():
    parser = argparse.ArgumentParser(
        description="Generador de datos sintéticos")  # q argumentos esperar
    parser.add_argument("--s", type=int, required=True,
                        help="Factor de escala")
    args = parser.parse_args()  # es la escala s de cada instancia

    carpeta_salida = RAIZ_PROYECTO / "datos" / "csv" / f"escala_{args.s}"
    random.seed(SEMILLA)
    np.random.seed(SEMILLA)
    fake = Faker()
    Faker.seed(SEMILLA)

    n_usuarios = BASE_USUARIOS * args.s
    n_artistas = BASE_ARTISTAS * args.s
    n_canciones = BASE_CANCIONES * args.s
    n_reproducciones = BASE_REPRODUCCIONES * args.s

    # descomentar para ver los tiempos de generar cada tabla
    inicio = time.time()
    df_usuarios = generar_usuarios(n_usuarios, fake)
    print(f"generar_usuarios tardó {time.time() - inicio:.2f} segundos")

    inicio = time.time()
    df_artistas = generar_artistas(n_artistas, fake)
    print(f"generar_artistas tardó {time.time() - inicio:.2f} segundos")

    inicio = time.time()
    df_generos = generar_generos()
    print(f"generar_generos tardó {time.time() - inicio:.2f} segundos")

    inicio = time.time()
    df_canciones = generar_canciones(n_canciones, df_artistas, df_generos)
    print(f"generar_canciones tardó {time.time() - inicio:.2f} segundos")

    guardar_csv(df_usuarios, "usuarios", carpeta_salida)
    guardar_csv(df_artistas, "artistas", carpeta_salida)
    guardar_csv(df_generos, "generos", carpeta_salida)
    guardar_csv(df_canciones, "canciones", carpeta_salida)
    inicio = time.time()
    guardar_reproducciones_csv(
        n_reproducciones, df_usuarios, df_canciones, TAMANO_CHUNK, "reproducciones", carpeta_salida)
    print(
        f"guardar_reproducciones_csv tardó {time.time() - inicio:.2f} segundos")


if __name__ == "__main__":
    main()
