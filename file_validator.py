# Responsabilidad única: validar que el archivo cumpla con las reglas

EXTENSION_PERMITIDA = ".py"
TAMANO_MAXIMO_BYTES = 2 * 1024 * 1024  #2 mb

def validar_extension(nombre_archivo: str) -> tuple[bool, str]:
    """
    Verifica que el archivo termina en .py
    Retorna (True, "") si es válido, o (False, "mensaje de error") si no.
    """
    if not nombre_archivo.endswith(EXTENSION_PERMITIDA):
        extension_enviada = nombre_archivo.split(".")[-1] if "." in nombre_archivo else "sin extensión"
        return False, f"Extensión '.{extension_enviada}' no permitida. Solo se aceptan archivos .py"
    return True, ""

def validar_tamano(tamano_bytes: int) -> tuple[bool, str]:
    """
    Verifica que el archivo no supere 2MB.
    """
    if tamano_bytes > TAMANO_MAXIMO_BYTES:
        tamano_mb = tamano_bytes / (1024 * 1024)
        return False, f"El archivo pesa {tamano_mb:.2f}MB. El máximo permitido es 2MB."
    return True, ""

def validar_archivo(nombre_archivo: str, tamano_bytes: int) -> tuple[bool, str]:
    """
    Función principal: ejecuta todas las validaciones en orden.
    Retorna (True, "") si todo está bien, o (False, "error") al primer problema.
    """
    ok, error = validar_extension(nombre_archivo)
    if not ok:
        return False, error

    ok, error = validar_tamano(tamano_bytes)
    if not ok:
        return False, error

    return True, ""