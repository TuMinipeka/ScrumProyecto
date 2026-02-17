# =============================================================
# main.py — Orquestador principal
# Historia #1: Carga de Archivos
# Historia #2: Configuración de Pruebas + Calificación
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
from test_case_ui import ejecutar_panel_profesor
from grader import calificar
from grader_ui import pedir_cod_tarea, mostrar_resultados


# ── Menú de rol ───────────────────────────────────────────────

def elegir_rol() -> str:
    print()
    print("  ¿Con qué rol ingresas?")
    print()
    print("  [1] Estudiante  — Entregar y calificar tarea")
    print("  [2] Profesor    — Configurar casos de prueba")
    print()
    while True:
        opcion = input("  Elige (1 o 2): ").strip()
        if opcion == "1":
            return "estudiante"
        if opcion == "2":
            return "profesor"
        print("  ⚠  Escribe 1 o 2.")


# ── Flujo del estudiante ──────────────────────────────────────

def flujo_estudiante():
    id_estudiante = pedir_id_estudiante()

    while True:
        # Paso 1: el estudiante elige su archivo
        ruta = elegir_archivo()

        # Paso 2: validar y registrar la entrega
        archivo_registrado = procesar_entrega(id_estudiante, ruta)

        # Paso 3: si la entrega fue válida, preguntar si quiere calificar
        if archivo_registrado:
            print()
            respuesta = input("  ¿Quieres calificar este archivo ahora? (s/n): ").strip().lower()
            if respuesta == "s":
                cod_tarea   = pedir_cod_tarea()
                calificacion = calificar(ruta, cod_tarea)

                if "error" in calificacion:
                    mostrar_error(calificacion["error"])
                else:
                    mostrar_resultados(calificacion)

        if not preguntar_continuar():
            break


def procesar_entrega(id_estudiante: str, ruta_archivo: str) -> bool:
    """
    Valida y registra la entrega.
    Retorna True si fue exitosa, False si falló.
    """
    mostrar_separador()

    nombre_archivo = os.path.basename(ruta_archivo)
    tamano_bytes   = os.path.getsize(ruta_archivo)

    es_valido, mensaje_error = validar_archivo(nombre_archivo, tamano_bytes)
    if not es_valido:
        mostrar_error(mensaje_error)
        return False

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
    return True


# ── Flujo del profesor ────────────────────────────────────────

def flujo_profesor():
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