# =============================================================
# file_browser.py
# Módulo 4 — Explorador de archivos desde consola
# Historia de Usuario #1: Carga de Archivos
# =============================================================
# Responsabilidad: permitir al estudiante navegar sus carpetas
# y elegir un archivo .py sin necesidad de escribir rutas.
#
# Flujo:
#   1. Muestra la carpeta actual con sus subcarpetas y .py
#   2. El estudiante elige un número
#   3. Si elige carpeta → entra a esa carpeta y repite
#   4. Si elige archivo → retorna la ruta completa
# =============================================================

import os


def _listar_contenido(carpeta: str) -> tuple:
    """
    Lista el contenido de una carpeta separando subcarpetas y archivos .py.

    Retorna:
        (subcarpetas, archivos_py)  ambas listas ordenadas alfabéticamente
    """
    try:
        entradas = os.listdir(carpeta)
    except PermissionError:
        return [], []

    subcarpetas = sorted([
        e for e in entradas
        if os.path.isdir(os.path.join(carpeta, e))
        and not e.startswith(".")          # ocultar carpetas ocultas
    ])

    archivos_py = sorted([
        e for e in entradas
        if os.path.isfile(os.path.join(carpeta, e))
        and e.lower().endswith(".py")
    ])

    return subcarpetas, archivos_py


def _mostrar_menu(carpeta_actual: str, subcarpetas: list, archivos_py: list):
    """
    Imprime el menú de navegación con números para cada opción.
    """
    print()
    print("=" * 56)
    print(f"  Ubicacion: {carpeta_actual}")
    print("=" * 56)

    opciones = []   # guardamos cada opción en orden para mapear el número

    # Opción 0: siempre mostrar "subir un nivel"
    print("  [0] .. (subir un nivel)")

    # Primero las carpetas
    if subcarpetas:
        print()
        print("  --- Carpetas ---")
        for nombre in subcarpetas:
            idx = len(opciones) + 1
            opciones.append(("carpeta", os.path.join(carpeta_actual, nombre)))
            print(f"  [{idx}] {nombre}/")

    # Luego los archivos .py
    if archivos_py:
        print()
        print("  --- Archivos .py ---")
        for nombre in archivos_py:
            idx = len(opciones) + 1
            ruta_completa = os.path.join(carpeta_actual, nombre)
            tamano_kb = os.path.getsize(ruta_completa) / 1024
            opciones.append(("archivo", ruta_completa))
            print(f"  [{idx}] {nombre}  ({tamano_kb:.1f} KB)")

    if not subcarpetas and not archivos_py:
        print()
        print("  (Esta carpeta no tiene archivos .py ni subcarpetas)")

    print()
    return opciones


def elegir_archivo() -> str:
    """
    Función principal del módulo.
    Permite al estudiante navegar carpetas y elegir un archivo .py.

    Retorna:
        str: ruta absoluta del archivo .py elegido
    """
    # Empezamos en la carpeta del usuario  C:\Users\danie
    carpeta_actual = os.path.expanduser("~")

    while True:
        subcarpetas, archivos_py = _listar_contenido(carpeta_actual)
        opciones = _mostrar_menu(carpeta_actual, subcarpetas, archivos_py)

        # Pedimos al estudiante que elija
        total = len(opciones)
        eleccion_str = input(f"  Elige una opcion (0 a {total}): ").strip()

        # Validamos que sea un número dentro del rango
        if not eleccion_str.isdigit():
            print("  ⚠  Escribe solo el numero de la opcion.")
            continue

        eleccion = int(eleccion_str)

        # Opción 0: subir un nivel
        if eleccion == 0:
            padre = os.path.dirname(carpeta_actual)
            if padre == carpeta_actual:
                print("  ⚠  Ya estas en la raiz, no puedes subir mas.")
            else:
                carpeta_actual = padre
            continue

        # Opción fuera de rango
        if eleccion > total:
            print(f"  ⚠  Elige un numero entre 0 y {total}.")
            continue

        tipo, ruta = opciones[eleccion - 1]

        # Si eligió carpeta → entramos a ella
        if tipo == "carpeta":
            carpeta_actual = ruta
            continue

        # Si eligió archivo → retornamos la ruta
        if tipo == "archivo":
            print(f"\n  Archivo seleccionado: {os.path.basename(ruta)}")
            return ruta