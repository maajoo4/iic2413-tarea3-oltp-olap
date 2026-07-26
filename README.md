# iic2413-tarea3-oltp-olap
Comparación experimental OLTP (PostgreSQL) vs OLAP (DuckDB) sobre una plataforma de streaming - modelado ER//BCNF/estrella, ETL, y benchmarks de escalabilidad.

---
### Integrante:
<small>
María José Cadenas Orta
<samll>

---
## 📁 Arquitectura del proyecto
| Archivo/Carpeta | Descripción |
|---|---|
| `Informe.pdf` | Parte A-E y visualizaciones |
| `modelo/schema_oltp.sql` | Creación de tablas en BCNF |
| `modelo/schema_estrella.sql` | Creación del esquema estrella para OLAP |
| `generador/` | Código generador de datos sintéticos |
| `README.md` | Instrucciones para ejecutar la aplicación |
---
## 💻 Tecnologías utilizadas
- PostgreSQL 17
- Python 3.12
- DuckDB
---
## 📚 Librerias utilizadas
---
### Librerias externas que deben ser instaladas:

```bash
pip install faker numpy pandas python-dotenv psycopg2-binary matplotlib
```

### Incluidas en la librería estándar de Python (no requieren instalación)
- argparse, subprocess, pathlib, os, time, random
--- 
## Pasos para correr la tarea:

## Configuración
<small>
Antes de ejecutar el proyecto, renombre el archivo `.env.example` a `.env` y modifique `PGUSER` con su usuario de postgres y `PGPASSWORD` con su contraseña para postgres. Estos datos serán usados en la función `conectar` declarada en el archivo `cargar_postgres`.
El archivo `.env` original **no se sube al repositorio**, ya que contiene credenciales sensibles.<small>

---
### 1. Generar los datos sintéticos con escalas diferentes:

Desde la raiz del proyecto correr por separado cada uno de los siguientes comandos que corresponden a la escala a ejecutar. Esto genera los archivos CSV de la instancia en `datos/csv/escala_n/` (usuarios, artistas, generos, canciones, reproducciones).

```bash
python -m generador.generar_datos --s 1   
python -m generador.generar_datos --s 5
python -m generador.generar_datos --s 10
python -m generador.generar_datos --s 50
python -m generador.generar_datos --s 1000
```
---
### 2. Cargar los datos en la base de datos según las escalas:

Crear la base de datos y cargar los datos según la escala una por una (separado). 
Con esto se crea la base de datos correspondiente (`db_streaming_escala{s}`) si no existe, carga el esquema OLTP, y carga los datos generados en el paso anterior usando `COPY`.
Para generar otras escalas, correr por separado cada uno de los siguientes comandos desde la raiz del proyecto:

```bash
python -m generador.cargar_oltp --s 1
python -m generador.cargar_oltp --s 5
python -m generador.cargar_oltp --s 10
python -m generador.cargar_oltp --s 50
python -m generador.cargar_oltp --s 1000
```
---
### 3. Transformacion OLTP -> Estrella y generación de archivos parquet según escalas:

Desde la raiz del proyecto correr por separado lo siguiente:

```bash
python -m etl.etl --s 1 
python -m etl.etl --s 5
python -m etl.etl --s 10
python -m etl.etl --s 50
python -m etl.etl --s 1000
```
---
### 4. Cargar los datos a Duckdb y verificar la equivalencia:

Desde la raiz del proyecto correr por separado lo siguiente:

```bash
python -m etl.verificar_equivalencia --s 1
python -m etl.verificar_equivalencia --s 5
python -m etl.verificar_equivalencia --s 10
python -m etl.verificar_equivalencia --s 50
python -m etl.verificar_equivalencia --s 1000
```
--- 
### 5. Correr los experimentos:
 Acá se presenta una limitación, por favor revisar detenidamente las siguientes instrucciones:

## ⚠️ Limitación de plataforma: reinicio de PostgreSQL

El script de experimentos (`experimentos/medir.py`) incluye la función `reiniciar_pg()` que reinicia automáticamente el servicio de PostgreSQL entre mediciones en frío. **Esta función solo funciona en Windows**, ya que utiliza PowerShell y el nombre de servicio específico de Windows (`postgresql-x64-17`).

### Si usas Windows

Verifica que el nombre de tu servicio coincida. Puedes confirmarlo con:
```powershell
Get-Service -Name "postgresql*"
```
Si tu servicio tiene un nombre distinto (por ejemplo, otra versión de PostgreSQL), ajusta el nombre dentro de `reiniciar_pg()` en `experimentos/medir.py`.

### Si usas Mac o Linux

Esta función no funcionará tal como está. Deberás reemplazar el contenido de `reiniciar_pg()` con el comando equivalente de tu sistema:

- **Linux (systemd):** `sudo systemctl restart postgresql`
- **Mac (Homebrew):** `brew services restart postgresql`
---
### 6. Generar gráficos 

Desde la raíz del proyecto ejecutar el siguiente comando:

```bash
python -m experimentos.analizar_resultados
```
---
# Consideraciones

- Los datos son generados sintéticamente y en algunos casos los datos son sinteticos (ej. nombre usuario : u1, u2, ...).
- El esquema OLTP corresponde al modelo transaccional diseñado en la Parte A.
- El esquema OLAP corresponde a un esquema estrella.
---
# Observaciones/Supuestos

**Consola:** cada vez que se corre un comando se imprimen datos respecto al tiempo de ejecución y mensajes descriptivos de cada una, con el fin de tener un poco de mayor detalle respecto a que se está ejecutando.

**Sobre las mediciones en frío (PostgreSQL):** el reinicio del servicio de PostgreSQL entre mediciones en frío vacía el buffer pool interno del motor, pero no purga el *page cache* del sistema operativo (Windows). Por ende, parte de los datos podrían seguir residiendo en la caché de disco incluso después del reinicio, lo que podría hacer que nuestras mediciones "en frío" sean ligeramente más optimistas de lo que serían en un escenario de frío absoluto.

**Sobre las mediciones en frío (DuckDB):** como DuckDB opera en memoria (`:memory:`) y no mantiene un servicio persistente, definí "frío" como la creación de una nueva conexión y la recarga completa de los archivos Parquet desde disco. Sin embargo, al igual que con PostgreSQL, esto no garantiza que dichos archivos estén fuera de la caché de disco del sistema operativo, por lo que la medición en frío de DuckDB podría también estar subestimando el costo real de un acceso verdaderamente en frío.

**Sobre el orden físico de los datos en Parquet:** las estadísticas min/max por row group (intrínsecas al formato Parquet) permiten a DuckDB descartar bloques completos cuando un filtro actúa sobre una columna físicamente ordenada. Para efectos de este proyecto, las dimensiones (`dim_usuario`, `dim_artista`, `dim_cancion`) se generaron con identificadores secuenciales, por lo que sí están ordenadas por su propia llave primaria, permitiendo cierta poda de bloques en consultas de alta selectividad sobre esas tablas. En cambio, la tabla de hechos (`fact_reproducciones`) contiene columnas como `id_usuario`, `id_cancion` y `dispositivo` asignadas de forma aleatoria, sin ningún orden físico, por lo que las consultas que filtran por dichas columnas no logran beneficiarse de esta optimización. Como mejora parcial, ordené cada *chunk* de la tabla de hechos por `tmsp` antes de exportarlo a Parquet, lo que permite cierta poda de bloques en consultas con filtro de rango de fechas, aunque el orden global entre archivos distintos (`_parte0.parquet`, `_parte1.parquet`, etc.) no está garantizado.

**Sobre la reproducibilidad del reinicio automático de PostgreSQL:** la función `reiniciar_pg()` utilizada para automatizar el reinicio del servicio entre mediciones en frío depende de PowerShell y del nombre de servicio específico de Windows (`postgresql-x64-17`), por lo que no es portable a otros sistemas operativos sin modificaciones. Esta limitación se documenta en detalle en la sección correspondiente del README.
