'''Funciones generadoras de datos sinteticos para cada tabla'''

import random
import pandas as pd
import numpy as np
from .config import GENEROS_FIJOS, DISPOSITIVOS
from .utils import escoger_genero, escoger_plan


def generar_usuarios(n_usuarios, fake):
    ids_usuario = np.arange(1, n_usuarios + 1)
    nombres = np.array(["u" + str(i) for i in ids_usuario])
    emails = np.array(["u" + str(i) + "@mail.com" for i in ids_usuario])
    paises = np.array([fake.country() for _ in range(n_usuarios)])
    planes = escoger_plan()

    ahora = np.datetime64("now")
    hace_3_anios = ahora - np.timedelta64(3 * 365, "D")
    segundos_totales = (ahora - hace_3_anios) / np.timedelta64(1, "s")
    offsets = np.random.random(n_usuarios) * segundos_totales
    fechas_registro = hace_3_anios + \
        offsets.astype(np.int64) * np.timedelta64(1, "s")

    df_usuarios = pd.DataFrame({
        "id_usuario": ids_usuario,
        "nombre": nombres,
        "email": emails,
        "pais": paises,
        "fecha_registro": fechas_registro,
        "plan": planes
    })

    return df_usuarios


def generar_artistas(n_artistas, fake):
    lista_artistas = []

    for i in range(n_artistas):
        id_artista = i + 1
        nombre = "a" + str(id_artista)
        pais = fake.country()
        genero_principal = escoger_genero()

        lista_artistas.append({"id_artista": id_artista,
                               "nombre": nombre,
                               "pais_origen": pais,
                               "genero_principal": genero_principal})
    return pd.DataFrame(lista_artistas)


def generar_generos():
    lista_generos = []

    for i, nombre in enumerate(GENEROS_FIJOS):
        id_genero = i + 1
        lista_generos.append({"id_genero": id_genero,
                              "nombre": nombre})
    return pd.DataFrame(lista_generos)


def generar_canciones(n_canciones, df_artistas, df_generos):
    ids_artistas = df_artistas["id_artista"].tolist()
    ids_generos = df_generos["id_genero"].tolist()
    lista_canciones = []

    for i in range(n_canciones):
        id_cancion = i + 1
        duracion = random.randint(60, 400)  # segundos promedio de una cancion
        titulo = "c" + str(id_cancion)
        id_artist = random.choice(ids_artistas)
        id_genero = random.choice(ids_generos)
        lista_canciones.append({"id_cancion": id_cancion,
                                "duracion": duracion,
                                "titulo": titulo,
                                "id_artista": id_artist,
                                "id_genero": id_genero})
    return pd.DataFrame(lista_canciones)


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
