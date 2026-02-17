# El q lo lea es gay

import os
import shutil

# -------------------------
# CONFIGURACIÓN
# -------------------------

CARPETA_DESTINO = "submissions"
LIMITE_TAMANO = 2 * 1024 * 1024  # 2MB

# Crear carpeta si no existe
if not os.path.exists(CARPETA_DESTINO):
    os.makedirs(CARPETA_DESTINO)


# -------------------------
# FUNCIONES
# -------------------------

def generar_id_entrega():
    """
    Genera un ID tipo:
    ENTREGA-0001
    ENTREGA-0002
    """
    archivos = os.listdir(CARPETA_DESTINO)
    cantidad = len(archivos) + 1
    return f"ENTREGA-{cantidad:04d}"


def validar_archivo(ruta):
    """
    Verifica:
    - Que exista
    - Que sea .py
    - Que no supere 2MB
    """
    if not os.path.exists(ruta):
        return False, "El archivo no existe."

    if not ruta.lower().endswith(".py"):
        return False, "Solo se permiten archivos .py"

    tamaño = os.path.getsize(ruta)

    if tamaño > LIMITE_TAMANO:
        return False, "El archivo supera el límite de 2MB"

    return True, ""


def subir_archivo(ruta):
    """
    Función principal que ejecuta todo el proceso
    """
    valido, mensaje = validar_archivo(ruta)

    if not valido:
        print("❌ Error:", mensaje)
        return

    id_entrega = generar_id_entrega()

    nueva_ruta = os.path.join(CARPETA_DESTINO, id_entrega + ".py")

    shutil.copy(ruta, nueva_ruta)

    print("✅ Archivo subido correctamente")
    print("ID de transacción:", id_entrega)


# -------------------------
# PROGRAMA PRINCIPAL
# -------------------------

if __name__ == "__main__":
    ruta_archivo = input("Ingrese la ruta del archivo .py que desea subir: ")
    subir_archivo(ruta_archivo)
