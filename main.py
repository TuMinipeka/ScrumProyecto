# =============================================================
# main.py
# Orquestador principal — Historia de Usuario #1: Carga de Archivos
# =============================================================
import os

from upload_ui import (
    mostrar_bienvenida, mostrar_separador, pedir_id_estudiante,
    mostrar_error, mostrar_exito, preguntar_continuar,
)
from file_validator import validar_archivo
from transaction_service import (
    generar_id_transaccion, guardar_registro, guardar_archivo_fisico,
)
from file_browser import elegir_archivo    # <-- nuevo módulo


def procesar_entrega(id_estudiante: str, ruta_archivo: str):
    """
    Ejecuta el flujo completo de una entrega dado un archivo ya localizado.
    """
    mostrar_separador()

    # ── PASO 1: Extraer nombre y tamaño ──────────────────────────
    nombre_archivo = os.path.basename(ruta_archivo)
    tamano_bytes   = os.path.getsize(ruta_archivo)

    # ── PASO 2: Validar extensión y tamaño ───────────────────────
    es_valido, mensaje_error = validar_archivo(nombre_archivo, tamano_bytes)
    if not es_valido:
        mostrar_error(mensaje_error)
        return

    # ── PASO 3: Leer contenido ───────────────────────────────────
    with open(ruta_archivo, "rb") as f:
        contenido = f.read()

    # ── PASO 4: Generar ID y guardar ─────────────────────────────
    id_transaccion = generar_id_transaccion()
    guardar_archivo_fisico(id_transaccion, nombre_archivo, contenido)
    registro = guardar_registro(
        id_transaccion=id_transaccion,
        nombre_archivo=nombre_archivo,
        tamano_bytes=tamano_bytes,
        id_estudiante=id_estudiante,
    )

    # ── PASO 5: Mostrar éxito ────────────────────────────────────
    mostrar_exito(registro)


def main():
    mostrar_bienvenida()
    id_estudiante = pedir_id_estudiante()

    while True:
        # El estudiante navega sus carpetas y elige el archivo
        ruta = elegir_archivo()
        procesar_entrega(id_estudiante, ruta)

        if not preguntar_continuar():
            print()
            print("  Sesion finalizada. Hasta pronto!")
            print()
            break


if __name__ == "__main__":
    main()