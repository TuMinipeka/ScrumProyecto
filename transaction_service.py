# Responsabilidad: generar IDs únicos y guardar registros de cada entrega

import uuid
import json
import os
from datetime import datetime

CARPETA_REGISTROS  = "registros_entregas"   # carpeta donde se guardan los JSON
CARPETA_ARCHIVOS   = "archivos_subidos"     # carpeta donde se guardan los .py

def _asegurar_carpetas():
    """Crea las carpetas si no existen. El _ indica que es de uso interno."""
    os.makedirs(CARPETA_REGISTROS, exist_ok=True)
    os.makedirs(CARPETA_ARCHIVOS,  exist_ok=True)

def generar_id_transaccion() -> str:
    """
    Genera un ID único usando UUID4 (aleatorio).
    Ejemplo resultado: "TXN-a3f8c1d2-4e5b-..."
    """
    return f"TXN-{uuid.uuid4()}"

def guardar_registro(id_transaccion: str, nombre_archivo: str,
    tamano_bytes: int, id_estudiante: str) -> dict:
    """
    Crea y guarda un archivo JSON con todos los datos de la entrega.
    Este registro es la base para la auditoría (Historia #3).
    """
    _asegurar_carpetas()

    registro = {
        "id_transaccion": id_transaccion,
        "id_estudiante":  id_estudiante,
        "nombre_archivo": nombre_archivo,
        "tamano_bytes":   tamano_bytes,
        "fecha_hora":     datetime.now().isoformat(),   # ej: "2025-02-16T14:30:00"
        "estado":         "RECIBIDO"
    }

    # Guardamos un JSON por cada entrega — fácil de auditar
    ruta_json = os.path.join(CARPETA_REGISTROS, f"{id_transaccion}.json")
    with open(ruta_json, "w", encoding="utf-8") as f:
        json.dump(registro, f, indent=4, ensure_ascii=False)

    return registro

def guardar_archivo_fisico(id_transaccion: str, nombre_original: str,
    contenido: bytes) -> str:
    """
    Guarda el .py del estudiante con un nombre único
    para que dos archivos llamados 'tarea.py' no se sobreescriban.
    """
    _asegurar_carpetas()

    # Nuevo nombre: "TXN-uuid4_tarea.py"
    nombre_unico   = f"{id_transaccion}_{nombre_original}"
    ruta_guardado  = os.path.join(CARPETA_ARCHIVOS, nombre_unico)

    with open(ruta_guardado, "wb") as f:
        f.write(contenido)

    return ruta_guardado