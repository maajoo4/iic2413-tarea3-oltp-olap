import random
import pandas as pd

from config import GENEROS_FIJOS
from utils import escoger_genero, escoger_plan


def generar_usuarios(n_usuarios, fake):
    lista_usuarios = []

    for i in range(n_usuarios):
        id_usuario = i + 1
        nombre = "u" + str(id_usuario)
        email = fake.email()
        pais = fake.country()
        fecha_registro = fake.date_time_between(
            start_date='-3y', end_date='now')
        plan = escoger_plan()
        lista_usuarios.append({"id_usuario": id_usuario,
                               "nombre": nombre,
                               "email": email,
                               "pais": pais,
                               "fecha_registro": fecha_registro,
                               "plan": plan})
    return pd.DataFrame(lista_usuarios)


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
