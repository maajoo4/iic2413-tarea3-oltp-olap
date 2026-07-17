'''Funcions para guardar datos a csv para el modelo OLTP'''
from pathlib import Path
from .generadores import generar_reproducciones


def guardar_csv(df, nombre, carpeta):
    Path(carpeta).mkdir(parents=True, exist_ok=True)

    df.to_csv(
        f"{carpeta}/{nombre}.csv",
        index=False
    )


def guardar_reproducciones_csv(n_reproducciones, df_usuarios, df_canciones, tamano_chunk, nombre, carpeta):
    Path(carpeta).mkdir(parents=True, exist_ok=True)
    ruta_archivo = f"{carpeta}/{nombre}.csv"

    contador = 0
    primera_vuelta = True

    while contador < n_reproducciones:
        cantidad = min(tamano_chunk, n_reproducciones - contador)
        id_inicial = contador + 1

        df_chunk = generar_reproducciones(
            id_inicial, cantidad, df_usuarios, df_canciones)

        df_chunk.to_csv(
            ruta_archivo,
            # si es la primera vez lo reescribe, sino hace append
            mode="w" if primera_vuelta else "a",
            header=primera_vuelta,
            index=False
        )

        contador += cantidad
        primera_vuelta = False

    print(f"Se generaron {contador} reproducciones en {ruta_archivo}")
