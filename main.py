# =============================================================
# main.py
# Orquestador principal — Sprint 1
# Historia #1: Carga de Archivos
# Historia #2: Configuración de Pruebas
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
from file_browser import elegir_archivo
from test_case_ui import ejecutar_panel_profesor   # Historia #2


# ── Menú de rol ───────────────────────────────────────────────

def elegir_rol() -> str:
    """
    Pregunta si el usuario es estudiante o profesor.

    Retorna:
        "estudiante" o "profesor"
    """
    print()
    print("  ¿Con qué rol ingresas?")
    print()
    print("  [1] Estudiante  — Entregar tarea")
    print("  [2] Profesor    — Configurar casos de prueba")
    print()
    while True:
        opcion = input("  Elige (1 o 2): ").strip()
        if opcion == "1":
            return "estudiante"
        if opcion == "2":
            return "profesor"
        print("  ⚠  Escribe 1 o 2.")


# ── Flujo del estudiante (Historia #1) ───────────────────────

def flujo_estudiante():
    """Flujo completo de entrega de archivo para el estudiante."""
    id_estudiante = pedir_id_estudiante()

    while True:
        ruta = elegir_archivo()
        procesar_entrega(id_estudiante, ruta)

        if not preguntar_continuar():
            break


def procesar_entrega(id_estudiante: str, ruta_archivo: str):
    mostrar_separador()

    nombre_archivo = os.path.basename(ruta_archivo)
    tamano_bytes   = os.path.getsize(ruta_archivo)

    es_valido, mensaje_error = validar_archivo(nombre_archivo, tamano_bytes)
    if not es_valido:
        mostrar_error(mensaje_error)
        return

    with open(ruta_archivo, "rb") as f:
        contenido = f.read()

    id_transaccion = generar_id_transaccion()
    guardar_archivo_fisico(id_transaccion, nombre_archivo, contenido)
    registro = guardar_registro(
        id_transaccion=id_transaccion,
        nombre_archivo=nombre_archivo,
        tamano_bytes=tamano_bytes,
        id_estudiante=id_estudiante,
    )
    mostrar_exito(registro)


# ── Flujo del profesor (Historia #2) ─────────────────────────

def flujo_profesor():
    """Flujo completo de configuración de pruebas para el profesor."""
    while True:
        ejecutar_panel_profesor()
        print()
        respuesta = input("  ¿Configurar otra tarea? (s/n): ").strip().lower()
        if respuesta != "s":
            break


# ── Punto de entrada ─────────────────────────────────────────

def main():
    mostrar_bienvenida()
    rol = elegir_rol()

    if rol == "estudiante":
        flujo_estudiante()
    elif rol == "profesor":
        flujo_profesor()

    print()
    print("  Sesion finalizada. Hasta pronto!")
    print()


if __name__ == "__main__":
    main()