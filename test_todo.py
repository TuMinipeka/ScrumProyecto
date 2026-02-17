# =============================================================
# test_todo.py
# Pruebas unitarias de todos los modulos del proyecto
# =============================================================
# Como ejecutarlo:
#   python test_todo.py
# =============================================================

import os
import json

# Contador global de resultados
total_pruebas = 0
total_pasadas = 0
total_falladas = 0


def prueba(descripcion: str, condicion: bool, detalle: str = ""):
    global total_pruebas, total_pasadas, total_falladas
    total_pruebas += 1
    if condicion:
        total_pasadas += 1
        print(f"  [PASO] {descripcion}")
    else:
        total_falladas += 1
        print(f"  [FALLO] {descripcion}")
        if detalle:
            print(f"          --> {detalle}")


def seccion(titulo: str):
    print()
    print("=" * 56)
    print(f"  MODULO: {titulo}")
    print("=" * 56)


# =============================================================
# PRUEBAS: file_validator.py
# =============================================================
def probar_file_validator():
    seccion("file_validator.py")
    from file_validator import validar_extension, validar_tamano, validar_archivo

    ok, _ = validar_extension("tarea.py")
    prueba("Acepta archivo .py", ok)

    ok, _ = validar_extension("TAREA.PY")
    prueba("Acepta .PY en mayusculas", ok)

    ok, err = validar_extension("tarea.docx")
    prueba("Rechaza .docx", not ok)
    prueba("El error menciona la extension", "docx" in err)

    ok, _ = validar_extension("tarea.java")
    prueba("Rechaza .java", not ok)

    ok, _ = validar_extension("tarea")
    prueba("Rechaza archivo sin extension", not ok)

    ok, _ = validar_tamano(1024)
    prueba("Acepta archivo de 1KB", ok)

    ok, _ = validar_tamano(2 * 1024 * 1024)
    prueba("Acepta archivo exacto de 2MB", ok)

    ok, err = validar_tamano(2 * 1024 * 1024 + 1)
    prueba("Rechaza archivo mayor a 2MB", not ok)
    prueba("El error menciona el tamano", "MB" in err)

    ok, _ = validar_tamano(0)
    prueba("Rechaza archivo vacio (0 bytes)", not ok)

    ok, _ = validar_archivo("tarea.py", 500)
    prueba("Valida correctamente un .py de 500 bytes", ok)

    ok, _ = validar_archivo("tarea.txt", 500)
    prueba("Rechaza .txt aunque el tamano sea valido", not ok)

    ok, _ = validar_archivo("tarea.py", 99999999)
    prueba("Rechaza .py demasiado pesado", not ok)


# =============================================================
# PRUEBAS: transaction_service.py
# =============================================================
def probar_transaction_service():
    seccion("transaction_service.py")
    from transaction_service import (
        generar_id_transaccion, guardar_registro, guardar_archivo_fisico
    )

    id1 = generar_id_transaccion()
    id2 = generar_id_transaccion()

    prueba("El ID empieza con 'TXN-'", id1.startswith("TXN-"))
    prueba("Dos IDs seguidos son diferentes (unicidad)", id1 != id2)
    prueba("El ID tiene mas de 10 caracteres", len(id1) > 10)

    id_t    = generar_id_transaccion()
    registro = guardar_registro(id_t, "tarea_test.py", 1024, "STU-TEST")

    prueba("El registro tiene id_transaccion", "id_transaccion" in registro)
    prueba("El registro tiene fecha_hora",     "fecha_hora"     in registro)
    prueba("El registro tiene tamano_legible", "tamano_legible" in registro)
    prueba("El estado es RECIBIDO",            registro["estado"] == "RECIBIDO")
    prueba("El id_estudiante es correcto",     registro["id_estudiante"] == "STU-TEST")

    ruta_json = os.path.join("registros_entregas", f"{id_t}.json")
    prueba("El archivo JSON existe en disco", os.path.isfile(ruta_json))

    if os.path.isfile(ruta_json):
        with open(ruta_json, "r") as f:
            datos = json.load(f)
        prueba("El JSON contiene el id correcto", datos["id_transaccion"] == id_t)

    contenido_prueba = b"print('hola mundo')\n"
    ruta_guardada    = guardar_archivo_fisico(id_t, "tarea_test.py", contenido_prueba)

    prueba("El archivo .py se guardo en disco", os.path.isfile(ruta_guardada))

    if os.path.isfile(ruta_guardada):
        with open(ruta_guardada, "rb") as f:
            contenido_leido = f.read()
        prueba("El contenido del archivo es identico al original",
               contenido_leido == contenido_prueba)


# =============================================================
# PRUEBAS: test_case_service.py
# =============================================================
def probar_test_case_service():
    seccion("test_case_service.py")
    from test_case_service import guardar_casos, cargar_casos, listar_tareas

    casos_prueba = [
        {"id": 1, "entrada": "2 3",  "esperado": "5",  "puntaje": 5.0},
        {"id": 2, "entrada": "10 5", "esperado": "15", "puntaje": 5.0},
    ]

    config = guardar_casos("TEST-UNIT", "PROF-TEST", casos_prueba)

    prueba("Retorna un diccionario",             isinstance(config, dict))
    prueba("El cod_tarea es correcto",           config["cod_tarea"]     == "TEST-UNIT")
    prueba("Cuenta los casos correctamente",     config["total_casos"]   == 2)
    prueba("Calcula el puntaje total",           config["puntaje_total"] == 10.0)

    ruta_json = os.path.join("casos_de_prueba", "TEST-UNIT.json")
    prueba("El JSON se guardo en disco",         os.path.isfile(ruta_json))

    cargado = cargar_casos("TEST-UNIT")
    prueba("Carga la tarea correctamente",       cargado is not None)
    prueba("Los casos cargados son 2",           len(cargado["casos"]) == 2)
    prueba("El primer caso tiene entrada '2 3'", cargado["casos"][0]["entrada"] == "2 3")
    prueba("El primer caso tiene puntaje 5.0",   cargado["casos"][0]["puntaje"] == 5.0)

    no_existe = cargar_casos("TAREA-QUE-NO-EXISTE")
    prueba("Retorna None si la tarea no existe", no_existe is None)

    tareas = listar_tareas()
    prueba("listar_tareas retorna una lista",        isinstance(tareas, list))
    prueba("La tarea TEST-UNIT aparece en la lista", "TEST-UNIT" in tareas)


# =============================================================
# PRUEBAS: grader.py
# =============================================================
def probar_grader():
    seccion("grader.py")
    from test_case_service import guardar_casos
    from grader import calificar

    guardar_casos("TEST-GRADER", "PROF-TEST", [
        {"id": 1, "entrada": "2 3",  "esperado": "5",  "puntaje": 5.0},
        {"id": 2, "entrada": "10 5", "esperado": "15", "puntaje": 5.0},
    ])

    # Carpeta temporal dentro del mismo proyecto — compatible con Windows y Linux
    carpeta_temp = os.path.join(os.getcwd(), "temp_tests")
    os.makedirs(carpeta_temp, exist_ok=True)

    ruta_correcto = os.path.join(carpeta_temp, "test_correcto.py")
    ruta_parcial  = os.path.join(carpeta_temp, "test_parcial.py")
    ruta_error    = os.path.join(carpeta_temp, "test_error.py")

    with open(ruta_correcto, "w") as f:
        f.write("a, b = map(int, input().split())\nprint(a + b)\n")

    with open(ruta_parcial, "w") as f:
        f.write("a, b = map(int, input().split())\n"
                "if a == 2:\n    print(a + b)\nelse:\n    print('mal')\n")

    with open(ruta_error, "w") as f:
        f.write("print(esto_no_existe)\n")

    # -- solucion correcta --
    resultado = calificar(ruta_correcto, "TEST-GRADER")
    prueba("Retorna dict con nota_obtenida", "nota_obtenida" in resultado)
    prueba("Nota correcta = 10.0",           resultado["nota_obtenida"] == 10.0)
    prueba("Porcentaje correcto = 100%",     resultado["porcentaje"]    == 100.0)
    prueba("Ambos casos pasaron",
           all(r["paso"] for r in resultado["resultados"]))

    # -- solucion parcial --
    resultado = calificar(ruta_parcial, "TEST-GRADER")
    prueba("Solucion parcial no da 10",  resultado["nota_obtenida"] < 10.0)
    prueba("Solucion parcial da mas de 0", resultado["nota_obtenida"] > 0.0)

    # -- programa con error --
    resultado = calificar(ruta_error, "TEST-GRADER")
    prueba("Programa con error da 0 pts", resultado["nota_obtenida"] == 0.0)
    prueba("Los resultados tienen campo error",
           any(r["error"] for r in resultado["resultados"]))

    # -- tarea inexistente --
    resultado = calificar(ruta_correcto, "TAREA-FANTASMA")
    prueba("Tarea inexistente retorna error", "error" in resultado)


# =============================================================
# RESUMEN FINAL
# =============================================================
def mostrar_resumen():
    print()
    print("=" * 56)
    print("  RESUMEN DE PRUEBAS")
    print("=" * 56)
    print(f"  Total   : {total_pruebas}")
    print(f"  Pasaron : {total_pasadas}")
    print(f"  Fallaron: {total_falladas}")
    print()
    if total_falladas == 0:
        print("  TODO FUNCIONA CORRECTAMENTE")
    else:
        print(f"  HAY {total_falladas} PRUEBA(S) CON PROBLEMAS")
        print("  Revisa los [FALLO] arriba para ver que corregir.")
    print("=" * 56)


# =============================================================
# PUNTO DE ENTRADA
# =============================================================
if __name__ == "__main__":
    print()
    print("=" * 56)
    print("  EJECUTANDO PRUEBAS DEL PROYECTO")
    print("=" * 56)

    probar_file_validator()
    probar_transaction_service()
    probar_test_case_service()
    probar_grader()
    mostrar_resumen()