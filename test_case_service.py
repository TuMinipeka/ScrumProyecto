# =============================================================
# test_case_service.py
# Módulo — Servicio de casos de prueba
# Historia de Usuario #2: Configuración de Pruebas
# =============================================================
# Responsabilidad: guardar y cargar los casos de prueba que
# el profesor define para cada tarea.
#
# Cada tarea tiene su propio archivo JSON con este formato:
#
# {
#     "cod_tarea": "TAREA-01",
#     "profesor":  "PROF-001",
#     "fecha_creacion": "2025-02-17T...",
#     "casos": [
#         {
#             "id": 1,
#             "entrada":  "2 3",
#             "esperado": "5",
#             "puntaje":  2.5
#         }
#     ],
#     "puntaje_total": 2.5
# }
#
# Librerías usadas (incluidas en Python, sin instalar nada):
#   - json     → guardar y leer archivos JSON
#   - os       → crear carpetas y manejar rutas
#   - datetime → registrar fecha y hora de creación
# =============================================================

import json
import os
from datetime import datetime


CARPETA_PRUEBAS = "casos_de_prueba"   # carpeta donde se guardan los JSON


def _asegurar_carpeta():
    """Crea la carpeta si no existe."""
    os.makedirs(CARPETA_PRUEBAS, exist_ok=True)


def guardar_casos(cod_tarea: str, id_profesor: str, casos: list) -> dict:
    """
    Guarda los casos de prueba de una tarea en un archivo JSON.

    Parámetros:
        cod_tarea   (str):  código único de la tarea, ej: "TAREA-01"
        id_profesor (str):  ID del profesor que la configura
        casos       (list): lista de diccionarios con los casos de prueba

    Cada caso en la lista debe tener:
        - entrada   (str):   lo que se le enviará al programa del estudiante
        - esperado  (str):   lo que el programa debe imprimir
        - puntaje   (float): puntos que vale este caso

    Retorna:
        dict: la configuración completa guardada
    """
    _asegurar_carpeta()

    # Calculamos el puntaje total sumando todos los casos
    # round(..., 2) evita errores de punto flotante como 2.5000000001
    puntaje_total = round(sum(caso["puntaje"] for caso in casos), 2)

    configuracion = {
        "cod_tarea":       cod_tarea,
        "id_profesor":     id_profesor,
        "fecha_creacion":  datetime.now().isoformat(),
        "total_casos":     len(casos),
        "puntaje_total":   puntaje_total,
        "casos":           casos
    }

    # Nombre del archivo: "TAREA-01.json"
    ruta_json = os.path.join(CARPETA_PRUEBAS, f"{cod_tarea}.json")
    with open(ruta_json, "w", encoding="utf-8") as f:
        json.dump(configuracion, f, indent=4, ensure_ascii=False)

    return configuracion


def cargar_casos(cod_tarea: str) -> dict:
    """
    Carga los casos de prueba de una tarea desde su JSON.
    La Historia #2 (calificación automática) usará esta función.

    Parámetros:
        cod_tarea (str): código de la tarea a buscar

    Retorna:
        dict: la configuración completa
        None: si la tarea no existe
    """
    ruta_json = os.path.join(CARPETA_PRUEBAS, f"{cod_tarea}.json")

    if not os.path.isfile(ruta_json):
        return None

    with open(ruta_json, "r", encoding="utf-8") as f:
        return json.load(f)


def listar_tareas() -> list:
    """
    Retorna una lista con todos los códigos de tarea configurados.
    Útil para que el profesor vea qué tareas ya tiene creadas.
    """
    _asegurar_carpeta()

    archivos = os.listdir(CARPETA_PRUEBAS)

    # Extraemos el nombre sin la extensión .json
    # Ejemplo: "TAREA-01.json" → "TAREA-01"
    return [a.replace(".json", "") for a in archivos if a.endswith(".json")]