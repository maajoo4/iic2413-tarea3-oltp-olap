import pandas as pd
from pathlib import Path
import numpy as np
from config import DISPOSITIVOS


def guardar_csv(df, nombre, carpeta):
    Path(carpeta).mkdir(parents=True, exist_ok=True)

    df.to_csv(
        f"{carpeta}/{nombre}.csv",
        index=False
    )


def generar_reproducciones(id_inicial, chunk, df_usuarios, df_canciones):
    # como es orden de decena de millones con numpy genera de una vez todos los índices aleatorios que se van a necesitar
    indices_usuarios = np.random.randint(
        0, len(df_usuarios), size=chunk)
    ids_usuario_elegidos = df_usuarios["id_usuario"].to_numpy()[
        indices_usuarios]
    fechas_registro_elegidas = df_usuarios["fecha_registro"].to_numpy()[
        indices_usuarios]

    indices_canciones = np.random.randint(
        0, len(df_canciones), size=chunk)
    ids_cancion_elegidas = df_canciones["id_cancion"].to_numpy()[
        indices_canciones]
    duraciones_elegidas = df_canciones["duracion"].to_numpy()[
        indices_canciones]

    # generar todo de forma vectorizada pq con un loop es ineficiente
    dispositivos = np.random.choice(DISPOSITIVOS, size=chunk)
    u = np.random.random(chunk)
    tiempos = (u * duraciones_elegidas).astype(np.int32) + 1

    ahora = np.datetime64("now")
    segundos_disponibles = (
        (ahora - fechas_registro_elegidas) / np.timedelta64(1, "s"))
    offset_aleatorio = (
        np.random.random(chunk) * segundos_disponibles
    ).astype(np.int64)

    timestamps = fechas_registro_elegidas + \
        offset_aleatorio * np.timedelta64(1, "s")

    ids_reproduccion = np.arange(id_inicial, id_inicial + chunk)
    df_reproducciones = pd.DataFrame({
        "id_reproduccion": ids_reproduccion,
        "id_usuario": ids_usuario_elegidos,
        "id_cancion": ids_cancion_elegidas,
        "tmsp": timestamps,
        "dispositivo": dispositivos,
        "tiempo": tiempos
    })

    return df_reproducciones


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
            mode="w" if primera_vuelta else "a",
            header=primera_vuelta,
            index=False
        )

        contador += cantidad
        primera_vuelta = False

    print(f"Se generaron {contador} reproducciones en {ruta_archivo}")
