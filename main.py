# =============================================================
# main.py
# Orquestador principal — Historia de Usuario #1: Carga de Archivos
# =============================================================
import os

from upload_ui import (
    mostrar_bienvenida, mostrar_separador, pedir_id_estudiante,
    pedir_ruta_archivo, mostrar_error, mostrar_exito, preguntar_continuar,
)
from file_validator import validar_archivo
from transaction_service import (
    generar_id_transaccion, guardar_registro, guardar_archivo_fisico,
)


def buscar_archivo(nombre_o_ruta: str) -> str:
    """
    Busca el archivo automáticamente en las carpetas más comunes de Windows.

    Busca en este orden:
      1. La ruta exacta que escribió el estudiante
      2. La carpeta donde está main.py (directorio actual)
      3. Escritorio  (Desktop / Escritorio)
      4. Documentos  (Documents / Documentos)
      5. Descargas   (Downloads / Descargas)
      6. OneDrive    (común en Windows 11)

    Retorna la ruta completa si lo encuentra, o None si no existe en ningún lado.
    """
    home = os.path.expanduser("~")   # C:\Users\TuNombre en Windows

    carpetas_a_buscar = [
        "",                                           # 1. Ruta exacta
        os.getcwd(),                                  # 2. Carpeta actual (donde está main.py)
        os.path.join(home, "Desktop"),                # 3. Escritorio inglés
        os.path.join(home, "Escritorio"),             # 3b. Escritorio español
        os.path.join(home, "Documents"),              # 4. Documentos inglés
        os.path.join(home, "Documentos"),             # 4b. Documentos español
        os.path.join(home, "Downloads"),              # 5. Descargas inglés
        os.path.join(home, "Descargas"),              # 5b. Descargas español
        os.path.join(home, "OneDrive", "Desktop"),    # 6. OneDrive Escritorio
        os.path.join(home, "OneDrive", "Documents"),  # 6b. OneDrive Documentos
    ]

    # Extraemos solo el nombre del archivo
    # Si escribió "C:\algo\tarea.py" → solo_nombre queda "tarea.py"
    solo_nombre = os.path.basename(nombre_o_ruta)

    for carpeta in carpetas_a_buscar:
        ruta_candidata = nombre_o_ruta if carpeta == "" else os.path.join(carpeta, solo_nombre)
        if os.path.isfile(ruta_candidata):
            return ruta_candidata   # encontrado

    return None   # no se encontró en ningún lugar


def procesar_entrega(id_estudiante: str, ruta_archivo: str):
    """
    Ejecuta el flujo completo de una entrega.
    """
    mostrar_separador()

    # ── PASO 1: Buscar el archivo automáticamente ────────────────
    ruta_real = buscar_archivo(ruta_archivo)

    if ruta_real is None:
        home = os.path.expanduser("~")
        mostrar_error(
            f"No se encontró '{os.path.basename(ruta_archivo)}' en ninguna carpeta conocida.\n"
            f"\n"
            f"  Buscamos en:\n"
            f"    La ruta que escribiste  : {ruta_archivo}\n"
            f"    Esta carpeta (actual)   : {os.getcwd()}\n"
            f"    Escritorio              : {os.path.join(home, 'Desktop')}\n"
            f"    Documentos              : {os.path.join(home, 'Documents')}\n"
            f"    Descargas               : {os.path.join(home, 'Downloads')}\n"
            f"\n"
            f"  Solucion mas facil:\n"
            f"    Copia tu archivo .py a la misma carpeta donde esta main.py\n"
            f"    y escribe solo el nombre: tarea.py"
        )
        return

    # Avisamos si lo encontramos en un lugar diferente al que escribió
    if os.path.abspath(ruta_real) != os.path.abspath(ruta_archivo):
        print(f"\n  Archivo encontrado en: {ruta_real}")

    # ── PASO 2: Extraer nombre y tamaño ──────────────────────────
    nombre_archivo = os.path.basename(ruta_real)
    tamano_bytes   = os.path.getsize(ruta_real)

    # ── PASO 3: Validar extensión y tamaño ───────────────────────
    es_valido, mensaje_error = validar_archivo(nombre_archivo, tamano_bytes)
    if not es_valido:
        mostrar_error(mensaje_error)
        return

    # ── PASO 4: Leer contenido ───────────────────────────────────
    with open(ruta_real, "rb") as f:
        contenido = f.read()

    # ── PASO 5: Generar ID y guardar ─────────────────────────────
    id_transaccion = generar_id_transaccion()
    guardar_archivo_fisico(id_transaccion, nombre_archivo, contenido)
    registro = guardar_registro(
        id_transaccion=id_transaccion,
        nombre_archivo=nombre_archivo,
        tamano_bytes=tamano_bytes,
        id_estudiante=id_estudiante,
    )

    # ── PASO 6: Mostrar éxito ────────────────────────────────────
    mostrar_exito(registro)


def main():
    mostrar_bienvenida()
    id_estudiante = pedir_id_estudiante()

    while True:
        ruta = pedir_ruta_archivo()
        procesar_entrega(id_estudiante, ruta)

        if not preguntar_continuar():
            print()
            print("  Sesion finalizada. Hasta pronto!")
            print()
            break


if __name__ == "__main__":
    main()