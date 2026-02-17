# =============================================================
# transaction_service.py
# Módulo 2 — Generación de IDs y registro de entregas
# Historia de Usuario #1: Carga de Archivos
# =============================================================
# Responsabilidad: generar un ID único por entrega y guardar
# el registro en JSON. Esto también alimenta la Historia #3
# (Auditoría Inalterable).
#
# Librerías usadas (todas incluidas en Python, sin instalar):
#   - uuid     → genera IDs únicos garantizados
#   - json     → guarda los registros en formato legible
#   - os       → crea carpetas y maneja rutas de archivos
#   - datetime → registra la fecha y hora exacta
# =============================================================

import uuid
import json
import os
from datetime import datetime


# Carpetas donde se guardarán los datos
CARPETA_REGISTROS = "registros_entregas"   # archivos JSON de auditoría
CARPETA_ARCHIVOS  = "archivos_subidos"     # los .py entregados por estudiantes


# ── Función auxiliar (privada) ────────────────────────────────
def _asegurar_carpetas():
    """
    Crea las carpetas necesarias si aún no existen.
    exist_ok=True significa "no falla si ya existe".
    El guión bajo al inicio indica que es de uso interno del módulo.
    """
    os.makedirs(CARPETA_REGISTROS, exist_ok=True)
    os.makedirs(CARPETA_ARCHIVOS,  exist_ok=True)


# ── Funciones públicas ────────────────────────────────────────
def generar_id_transaccion() -> str:
    """
    Genera un ID único usando UUID versión 4 (completamente aleatorio).

    uuid.uuid4() produce algo como: a3f8c1d2-4e5b-4c3a-9d2e-1f5b8c3d7e9a
    Le agregamos el prefijo "TXN-" para que sea fácil de identificar.

    Ejemplo de resultado: "TXN-a3f8c1d2-4e5b-4c3a-9d2e-1f5b8c3d7e9a"

    ¿Por qué UUID? Porque si 300 estudiantes suben archivos al mismo
    tiempo, es matemáticamente imposible que dos IDs sean iguales.
    """
    return f"TXN-{uuid.uuid4()}"


def guardar_registro(id_transaccion: str, nombre_archivo: str,
                     tamano_bytes: int, id_estudiante: str) -> dict:
    """
    Crea un archivo JSON con todos los datos de la entrega.
    Un archivo JSON por entrega → fácil de buscar, leer y auditar.

    Parámetros:
        id_transaccion (str): ID único generado por generar_id_transaccion()
        nombre_archivo (str): nombre original del archivo, ej: "tarea1.py"
        tamano_bytes   (int): peso en bytes
        id_estudiante  (str): identificador del estudiante

    Retorna:
        dict: el registro completo que se guardó
    """
    _asegurar_carpetas()

    # Construimos el registro como un diccionario Python
    registro = {
        "id_transaccion": id_transaccion,
        "id_estudiante":  id_estudiante,
        "nombre_archivo": nombre_archivo,
        "tamano_bytes":   tamano_bytes,
        "tamano_legible": f"{tamano_bytes / 1024:.1f} KB",
        "fecha_hora":     datetime.now().isoformat(),   # "2025-02-16T14:30:00.123456"
        "estado":         "RECIBIDO"
        # Aquí la Historia #3 agregará: ip, hash_archivo, etc.
    }

    # Guardamos el diccionario como archivo JSON
    # El nombre del JSON es el mismo ID → fácil de encontrar después
    ruta_json = os.path.join(CARPETA_REGISTROS, f"{id_transaccion}.json")
    with open(ruta_json, "w", encoding="utf-8") as archivo_json:
        json.dump(registro, archivo_json, indent=4, ensure_ascii=False)
        # indent=4      → el JSON queda indentado y legible para humanos
        # ensure_ascii  → permite guardar caracteres como tildes

    return registro


def guardar_archivo_fisico(id_transaccion: str, nombre_original: str,
                           contenido: bytes) -> str:
    """
    Guarda el archivo .py del estudiante en disco con un nombre único.

    El problema de guardar solo "tarea.py": si 200 estudiantes
    suben "tarea.py", se sobreescriben entre sí.
    La solución: renombrar a "TXN-uuid4_tarea.py" → siempre único.

    Parámetros:
        id_transaccion (str): ID único para el nombre del archivo
        nombre_original (str): nombre original del archivo del estudiante
        contenido (bytes): contenido binario del archivo

    Retorna:
        str: ruta completa donde quedó guardado el archivo
    """
    _asegurar_carpetas()

    nombre_unico  = f"{id_transaccion}_{nombre_original}"
    ruta_destino  = os.path.join(CARPETA_ARCHIVOS, nombre_unico)

    # Escribimos en modo binario "wb" para no alterar el contenido
    with open(ruta_destino, "wb") as archivo:
        archivo.write(contenido)

    return ruta_destino