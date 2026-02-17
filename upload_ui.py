# =============================================================
# upload_ui.py
# Módulo 3 — Interfaz de usuario en consola
# Historia de Usuario #1: Carga de Archivos
# =============================================================
# Responsabilidad: todo lo que el estudiante ve y teclea.
# Este módulo NO tiene lógica de negocio. Solo muestra cosas
# y recoge datos. Así, si mañana quieren hacer una versión web,
# solo cambian este módulo sin tocar los otros dos.
# =============================================================

import os


def mostrar_bienvenida():
    """Muestra el encabezado del sistema."""
    print()
    print("=" * 52)
    print("   SISTEMA DE ENTREGA DE TAREAS — PYTHON v1.0")
    print("   Universidad — Ciencias de la Computación")
    print("=" * 52)


def mostrar_separador():
    """Línea divisoria para organizar visualmente la consola."""
    print("-" * 52)


def pedir_id_estudiante() -> str:
    """
    Solicita el ID del estudiante.
    No avanza hasta que el usuario escriba algo.

    Retorna:
        str: el ID del estudiante (sin espacios al inicio/final)
    """
    print()
    while True:
        id_est = input("Ingresa tu ID de estudiante: ").strip()
        if id_est:
            return id_est
        # Si presionó Enter sin escribir nada, pedimos de nuevo
        print("  ⚠  El ID no puede estar vacío. Intenta de nuevo.")


def pedir_ruta_archivo() -> str:
    """
    Solicita la ruta del archivo .py al estudiante.
    Limpia automáticamente comillas, espacios y barras mixtas.

    Retorna:
        str: la ruta del archivo limpia y normalizada
    """
    print()
    print("Escribe la ruta de tu archivo .py (o solo el nombre si está en la misma carpeta)")
    print("  Windows : C:\\Users\\ana\\tarea.py")
    print("  Mac/Linux: /home/ana/tarea.py")
    print("  Misma carpeta: tarea.py")
    while True:
        ruta = input("> ").strip()

        # Eliminamos comillas que Windows/Mac agregan al arrastrar archivos
        ruta = ruta.strip('"').strip("'")

        # En Windows a veces copian rutas con barras invertidas dobles \\
        # os.path.normpath las convierte al formato correcto del sistema
        ruta = os.path.normpath(ruta)

        if ruta and ruta != ".":
            return ruta
        print("  ⚠  La ruta no puede estar vacía. Intenta de nuevo.")


def mostrar_error(mensaje: str):
    """
    Muestra un error al usuario de forma clara y visible.

    Parámetros:
        mensaje (str): descripción del problema
    """
    print()
    print("  ❌ ERROR")
    print(f"  {mensaje}")
    print()


def mostrar_exito(registro: dict):
    """
    Criterio de aceptación #3: mensaje de éxito con ID de transacción.

    Muestra todos los datos de la entrega para que el estudiante
    tenga constancia de que su tarea fue recibida correctamente.

    Parámetros:
        registro (dict): el registro retornado por guardar_registro()
    """
    print()
    print("✅ " * 18)
    print()
    print("       ENTREGA RECIBIDA EXITOSAMENTE")
    print()
    print(f"  ID de Transacción : {registro['id_transaccion']}")
    print(f"  Estudiante        : {registro['id_estudiante']}")
    print(f"  Archivo           : {registro['nombre_archivo']}")
    print(f"  Tamaño            : {registro['tamano_legible']}")
    print(f"  Fecha y hora      : {registro['fecha_hora']}")
    print(f"  Estado            : {registro['estado']}")
    print()
    print("  📌 IMPORTANTE: Guarda tu ID de transacción.")
    print("     Lo necesitarás para consultar el estado de tu entrega.")
    print()
    print("✅ " * 18)


def preguntar_continuar() -> bool:
    """
    Pregunta si el estudiante quiere subir otro archivo.

    Retorna:
        True  → quiere subir otro archivo
        False → quiere salir
    """
    print()
    respuesta = input("¿Deseas subir otro archivo? (s/n): ").strip().lower()
    return respuesta == "s"