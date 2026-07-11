import pandas as pd
import time
import random
import numpy as np
from datetime import datetime
from faker import Faker
from config import BASE_ARTISTAS, BASE_CANCIONES, BASE_REPRODUCCIONES, BASE_USUARIOS, SEMILLA, GENEROS_FIJOS, DISPOSITIVOS
import argparse
from utils import escoger_plan, escoger_genero
parser = argparse.ArgumentParser(
    description="Generador de datos sintéticos")  # q argumentos esperar
parser.add_argument("--s", type=int, required=True, help="Factor de escala")
args = parser.parse_args()  # es la escala s de cada instancia

random.seed(SEMILLA)
np.random.seed(SEMILLA)
fake = Faker()
Faker.seed(SEMILLA)

n_usuarios = BASE_USUARIOS * args.s
n_artistas = BASE_ARTISTAS * args.s
n_canciones = BASE_CANCIONES * args.s
n_reproducciones = BASE_REPRODUCCIONES * args.s


def generar_usuarios(n_usuarios):
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


def generar_artistas(n_artistas):
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


def generar_reproducciones(n_reproducciones, df_usuarios, df_canciones):
    # como es orden de decena de millones con numpy genera de una vez todos los índices aleatorios que se van a necesitar
    indices_usuarios = np.random.randint(
        0, len(df_usuarios), size=n_reproducciones)
    ids_usuario_elegidos = df_usuarios["id_usuario"].to_numpy()[
        indices_usuarios]
    fechas_registro_elegidas = df_usuarios["fecha_registro"].to_numpy()[
        indices_usuarios]

    indices_canciones = np.random.randint(
        0, len(df_canciones), size=n_reproducciones)
    ids_cancion_elegidas = df_canciones["id_cancion"].to_numpy()[
        indices_canciones]
    duraciones_elegidas = df_canciones["duracion"].to_numpy()[
        indices_canciones]

    # generar todo de forma vectorizada pq con un loop es ineficiente
    dispositivos = np.random.choice(DISPOSITIVOS, size=n_reproducciones)
    u = np.random.random(n_reproducciones)
    tiempos = (u * duraciones_elegidas).astype(np.int32) + 1

    ahora = np.datetime64("now")
    segundos_disponibles = (
        (ahora - fechas_registro_elegidas) / np.timedelta64(1, "s"))
    offset_aleatorio = (
        np.random.random(n_reproducciones) * segundos_disponibles
    ).astype(np.int64)

    timestamps = fechas_registro_elegidas + \
        offset_aleatorio * np.timedelta64(1, "s")

    ids_reproduccion = np.arange(1, n_reproducciones + 1)
    df_reproducciones = pd.DataFrame({
        "id_reproduccion": ids_reproduccion,
        "id_usuario": ids_usuario_elegidos,
        "id_cancion": ids_cancion_elegidas,
        "tmsp": timestamps,
        "dispositivo": dispositivos,
        "tiempo": tiempos
    })

    return df_reproducciones


inicio = time.time()
df_usuarios = generar_usuarios(n_usuarios)
print(f"generar_usuarios tardó {time.time() - inicio:.2f} segundos")

inicio = time.time()
df_artistas = generar_artistas(n_artistas)
print(f"generar_artistas tardó {time.time() - inicio:.2f} segundos")

inicio = time.time()
df_generos = generar_generos()
print(f"generar_generos tardó {time.time() - inicio:.2f} segundos")

inicio = time.time()
df_canciones = generar_canciones(n_canciones, df_artistas, df_generos)
print(f"generar_canciones tardó {time.time() - inicio:.2f} segundos")

inicio = time.time()
df_reproducciones = generar_reproducciones(
    n_reproducciones, df_usuarios, df_canciones)
print(f"generar_reproducciones tardó {time.time() - inicio:.2f} segundos")

print(df_usuarios.iloc[1])
