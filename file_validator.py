# =============================================================
# file_validator.py
# Módulo 1 — Validación de archivos
# Historia de Usuario #1: Carga de Archivos
# =============================================================
# Responsabilidad única: verificar que el archivo cumple las
# reglas del negocio ANTES de guardarlo.
# No sabe nada de interfaz, ni de base de datos, ni de red.
# =============================================================

EXTENSION_PERMITIDA  = ".py"
TAMANO_MAXIMO_BYTES  = 2 * 1024 * 1024   # 2 MB = 2,097,152 bytes


def validar_extension(nombre_archivo: str) -> tuple:
    """
    Criterio #1: Solo se aceptan archivos .py

    Parámetros:
        nombre_archivo (str): nombre del archivo, ej: "tarea1.py"

    Retorna:
        (True, "")            → extensión válida
        (False, "mensaje")    → extensión inválida
    """
    if not nombre_archivo.lower().endswith(EXTENSION_PERMITIDA):
        # Extraemos la extensión para mostrarla en el error
        if "." in nombre_archivo:
            ext_enviada = nombre_archivo.rsplit(".", 1)[-1]   # lo que hay después del último punto
            mensaje = f"Extensión '.{ext_enviada}' no permitida. Solo se aceptan archivos .py"
        else:
            mensaje = "El archivo no tiene extensión. Solo se aceptan archivos .py"
        return False, mensaje

    return True, ""


def validar_tamano(tamano_bytes: int) -> tuple:
    """
    Criterio #2: El archivo no puede pesar más de 2MB.

    Parámetros:
        tamano_bytes (int): peso del archivo en bytes

    Retorna:
        (True, "")            → tamaño válido
        (False, "mensaje")    → demasiado pesado
    """
    if tamano_bytes > TAMANO_MAXIMO_BYTES:
        tamano_mb = tamano_bytes / (1024 * 1024)   # convertimos a MB para el mensaje
        mensaje = (
            f"El archivo pesa {tamano_mb:.2f} MB. "
            f"El tamaño máximo permitido es 2 MB."
        )
        return False, mensaje

    if tamano_bytes == 0:
        return False, "El archivo está vacío. No se puede entregar un archivo sin contenido."

    return True, ""


def validar_archivo(nombre_archivo: str, tamano_bytes: int) -> tuple:
    """
    Función principal del módulo.
    Ejecuta TODAS las validaciones en orden y retorna al primer error.

    Parámetros:
        nombre_archivo (str): nombre del archivo con su extensión
        tamano_bytes   (int): peso del archivo en bytes

    Retorna:
        (True, "")            → archivo válido, se puede procesar
        (False, "mensaje")    → archivo inválido, mostrar mensaje al usuario
    """
    # Primero verificamos la extensión
    ok, error = validar_extension(nombre_archivo)
    if not ok:
        return False, error

    # Luego verificamos el tamaño
    ok, error = validar_tamano(tamano_bytes)
    if not ok:
        return False, error

    # Si pasó todas las validaciones, el archivo es válido
    return True, ""