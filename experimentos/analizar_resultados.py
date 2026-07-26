from .utils import RUTA_CSV
import pandas as pd
from .graficar import generar_graficos

def main():
    df = pd.read_csv(RUTA_CSV)
    generar_graficos(df, "caliente")
    generar_graficos(df, "frio")


if __name__ == "__main__":
    main()
    
