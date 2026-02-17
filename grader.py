# =============================================================
# grader.py
# Módulo — Motor de calificación automática
# Conecta Historia #1 (archivo subido) con Historia #2 (casos)
# =============================================================
# Responsabilidad: ejecutar el archivo .py del estudiante con
# cada caso de prueba del profesor y calcular la nota final.
#
# Librería usada:
#   - subprocess → ejecuta programas externos desde Python
#                  Es la forma estándar de correr un .py desde otro .py
# =============================================================

import subprocess
import os
from test_case_service import cargar_casos


# Tiempo máximo que tiene el programa del estudiante para responder
# Si tarda más (bucle infinito, etc.) se cancela automáticamente
TIEMPO_LIMITE_SEGUNDOS = 5


def ejecutar_programa(ruta_py: str, entrada: str) -> dict:
    """
    Ejecuta un archivo .py con una entrada específica y captura su salida.

    Así funciona subprocess:
        Es como si abrieras una terminal, escribieras:
            python tarea.py
        y luego le enviaras el texto de 'entrada' como si lo escribiera el usuario.

    Parámetros:
        ruta_py (str): ruta al archivo .py del estudiante
        entrada (str): texto que se enviará como input() al programa

    Retorna dict con:
        - salida    (str):  lo que imprimió el programa (stdout)
        - error     (str):  mensaje de error si falló (stderr)
        - timeout   (bool): True si el programa tardó más de 5 segundos
        - excepcion (bool): True si el programa lanzó una excepción
    """
    try:
        resultado = subprocess.run(
            ["python", ruta_py],   # comando: python archivo.py
            input=entrada,         # lo que recibe el input() del estudiante
            capture_output=True,   # captura print() y errores
            text=True,             # trabaja con strings, no bytes
            timeout=TIEMPO_LIMITE_SEGUNDOS
        )
        return {
            "salida":    resultado.stdout.strip(),  # quitamos saltos de línea al final
            "error":     resultado.stderr.strip(),
            "timeout":   False,
            "excepcion": resultado.returncode != 0  # returncode != 0 significa que hubo error
        }

    except subprocess.TimeoutExpired:
        # El programa del estudiante tardó más de 5 segundos
        return {
            "salida":    "",
            "error":     f"El programa tardo mas de {TIEMPO_LIMITE_SEGUNDOS} segundos.",
            "timeout":   True,
            "excepcion": False
        }

    except Exception as e:
        return {
            "salida":    "",
            "error":     str(e),
            "timeout":   False,
            "excepcion": True
        }


def calificar(ruta_py: str, cod_tarea: str) -> dict:
    """
    Función principal del módulo.
    Ejecuta el archivo del estudiante contra TODOS los casos de prueba
    y devuelve el resultado completo de la calificación.

    Parámetros:
        ruta_py   (str): ruta al archivo .py del estudiante
        cod_tarea (str): código de la tarea, ej: "TAREA-01"

    Retorna dict con:
        - cod_tarea       (str)
        - nombre_archivo  (str)
        - nota_obtenida   (float): puntaje total ganado
        - nota_maxima     (float): puntaje máximo posible
        - porcentaje      (float): nota en porcentaje 0-100
        - resultados      (list):  detalle de cada caso
    """
    # Cargamos los casos que configuró el profesor
    config = cargar_casos(cod_tarea)
    if config is None:
        return {"error": f"No existe configuracion para la tarea '{cod_tarea}'"}

    nombre_archivo = os.path.basename(ruta_py)
    resultados     = []
    nota_obtenida  = 0.0

    # Ejecutamos el programa una vez por cada caso de prueba
    for caso in config["casos"]:
        ejecucion = ejecutar_programa(ruta_py, caso["entrada"])

        salida_real    = ejecucion["salida"]
        salida_esperada = caso["esperado"].strip()

        # Comparamos ignorando mayúsculas/minúsculas y espacios extras
        # Así "Hola " y "hola" se consideran iguales
        paso = (salida_real.lower().strip() == salida_esperada.lower().strip())

        # Solo sumamos puntos si pasó
        puntos_obtenidos = caso["puntaje"] if paso else 0.0
        nota_obtenida   += puntos_obtenidos

        resultados.append({
            "caso_id":          caso["id"],
            "entrada":          caso["entrada"],
            "esperado":         salida_esperada,
            "obtenido":         salida_real,
            "paso":             paso,
            "puntaje_posible":  caso["puntaje"],
            "puntaje_obtenido": puntos_obtenidos,
            "error":            ejecucion["error"],
            "timeout":          ejecucion["timeout"],
        })

    nota_obtenida = round(nota_obtenida, 2)
    nota_maxima   = config["puntaje_total"]

    # Porcentaje: si nota máxima es 0 evitamos división por cero
    porcentaje = round((nota_obtenida / nota_maxima) * 100, 1) if nota_maxima > 0 else 0.0

    return {
        "cod_tarea":      cod_tarea,
        "nombre_archivo": nombre_archivo,
        "nota_obtenida":  nota_obtenida,
        "nota_maxima":    nota_maxima,
        "porcentaje":     porcentaje,
        "resultados":     resultados,
    }