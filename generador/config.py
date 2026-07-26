'''Valores fijos que no cambian en las ejecuciones'''

from pathlib import Path

SEMILLA = 42
BASE_USUARIOS = 1000
BASE_ARTISTAS = 100
BASE_CANCIONES = 1000
BASE_REPRODUCCIONES = 10000
GENEROS_FIJOS = ["rock", "pop", "jazz",
                 "clasica", "reggaeton", "trap", "salsa"]
PLANES = ['free', 'premium', 'familiar']
DISPOSITIVOS = ['movil', 'web', 'smarttv']
TAMANO_CHUNK = 500000
CARPETA_ACTUAL = Path(__file__).parent
RAIZ_PROYECTO = CARPETA_ACTUAL.parent
RUTA_SCHEMA_OLTP = RAIZ_PROYECTO / "modelo" / "schema_oltp.sql"
TABLAS = ["usuarios", "artistas", "generos", "canciones", "reproducciones"]
COLUMNAS = {
    "usuarios": ["id_usuario", "nombre", "email", "pais", "fecha_registro", "plan"],
    "artistas": ["id_artista", "nombre", "pais_origen", "genero_principal"],
    "generos": ["id_genero", "nombre"],
    "canciones": ["id_cancion", "duracion", "titulo", "id_artista", "id_genero"],
    "reproducciones": ["id_reproduccion", "id_usuario", "id_cancion", "tmsp", "dispositivo", "tiempo"],
}
