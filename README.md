# iic2413-tarea3-oltp-olap
Comparación experimental OLTP (PostgreSQL) vs OLAP (DuckDB) sobre una plataforma de streaming - modelado ER//BCNF/estrella, ETL, y benchmarks de escalabilidad.

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
## 📚 Librerias necesarias 
- Faker
- Numpy
- Pandas 
- Python-dotenv
- Psycopg2-binary
--- 
## Pasos para correr la tarea:

## Configuración

Antes de ejecutar el proyecto, renombre el archivo `.env.example` a `.env` y modifique `PGUSER` con su usuario de postgres y `PGPASSWORD` con su contraseña para postgres. Estos datos serán usados en la función `conectar` declarada en el archivo `cargar_postgres`.
El archivo `.env` original **no se sube al repositorio** (está incluido en `.gitignore`), ya que contiene credenciales sensibles.

### 1. Generar los datos sintéticos con escalas diferentes
-- Desde la ruta en generador/ correr por separado cada uno de los siguientes comandos que corresponden a la escala a ejecutar. Esto genera los archivos CSV de la instancia en `datos/csv/escala_1/` (usuarios, artistas, generos, canciones, reproducciones).

```bash
python generar_datos.py --s 1  
python generar_datos.py --s 10
python generar_datos.py --s 100
python generar_datos.py --s 1000
python generar_datos.py --s 10000   
```
---
### 2. Cargar los datos en la base de datos según las escalas

Crear la base de datos y cargar los datos segun la escala una por una (separado). 
Con esto se crea la base de datos correspondiente (`db_streaming_escala{s}`) si no existe, carga el esquema OLTP, y carga los datos generados en el paso anterior usando `COPY`.
Para generar otras escalas, cambia el valor de `--s`. Las propuestas son las siguientes:

```bash
python cargar_postgres.py --s 1
python cargar_postgres.py --s 10
python cargar_postgres.py --s 100
python cargar_postgres.py --s 1000
python cargar_postgres.py --s 10000
```

# Consideraciones

- Los datos son generados sintéticamente.
- El esquema OLTP corresponde al modelo transaccional diseñado en la Parte A.
- El esquema OLAP corresponde a un esquema estrella.
- Las consultas analíticas fueron implementadas tanto sobre PostgreSQL como sobre DuckDB para verificar equivalencia y comparar rendimiento.

---

# Observaciones/Supuestos
