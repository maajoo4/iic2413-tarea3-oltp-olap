'''Script principal para verificar la equivalencia en el modelo OLTP y OLAP'''
import argparse
from .equivalencia import verificar_equivalencia


def main():
    parser = argparse.ArgumentParser(
        description="Verifica equivalencia entre OLTP y OLAP"
    )

    parser.add_argument(
        "--s",
        type=int,
        required=True,
        help="Escala de la instancia a verificar"
    )

    args = parser.parse_args()

    pasa = verificar_equivalencia(args.s)

    if pasa:
        print("\nVERIFICACIÓN FINAL: PASA")
    else:
        print("\nVERIFICACIÓN FINAL: FALLA")


if __name__ == "__main__":
    main()
