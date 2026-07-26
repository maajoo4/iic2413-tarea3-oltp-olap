import matplotlib.pyplot as plt
from generador.config import BASE_REPRODUCCIONES
from .utils import RAIZ

def generar_graficos(df, regimen):
    resumen = df[df["regimen"] == regimen].groupby(["escala", "motor", "clase"])["tiempo"].median()
    resumen = resumen.reset_index()
    resumen["n_reproducciones"] = resumen["escala"] * BASE_REPRODUCCIONES

    clases = resumen["clase"].unique()

    for clase in clases:
        datos_clase = resumen[resumen["clase"] == clase]

        datos_oltp = datos_clase[datos_clase["motor"] == "oltp"].sort_values("n_reproducciones")
        datos_olap = datos_clase[datos_clase["motor"] == "estrella"].sort_values("n_reproducciones")

        plt.figure()
        plt.plot(datos_oltp["n_reproducciones"], datos_oltp["tiempo"], marker="o", label="OLTP (PostgreSQL)")
        plt.plot(datos_olap["n_reproducciones"], datos_olap["tiempo"], marker="o", label="OLAP (DuckDB)")

        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("Tamaño de la instancia (número de reproducciones)")
        plt.ylabel("Tiempo (segundos)")
        plt.title(f"Tiempo vs tamaño de instancia ({regimen}) - Clase: {clase}")
        plt.legend()
        plt.grid(True, which="both", linestyle="--", alpha=0.5)

        ruta_figura = RAIZ / "resultados" / "figuras" / regimen / f"{clase}.png"
        ruta_figura.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(ruta_figura)
        plt.close()

        print(f"Gráfico guardado generado correctamente, visualizar en resultados")


