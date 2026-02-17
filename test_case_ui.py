# =============================================================
# test_case_ui.py
# Módulo — Interfaz del profesor para configurar casos de prueba
# Historia de Usuario #2: Configuración de Pruebas
# =============================================================
# Responsabilidad: guiar al profesor paso a paso para crear
# los casos de prueba de una tarea desde la consola.
#
# Flujo:
#   1. Pedir código de tarea
#   2. Ver tareas ya existentes
#   3. Agregar casos uno por uno (entrada, esperado, puntaje)
#   4. Confirmar y guardar
# =============================================================

from test_case_service import guardar_casos, cargar_casos, listar_tareas


# ── Pantallas informativas ────────────────────────────────────

def mostrar_encabezado_profesor():
    print()
    print("=" * 56)
    print("   PANEL DEL PROFESOR — Configuracion de Pruebas")
    print("=" * 56)


def mostrar_tareas_existentes():
    """Muestra las tareas que el profesor ya tiene configuradas."""
    tareas = listar_tareas()
    print()
    if not tareas:
        print("  (Aun no tienes tareas configuradas)")
    else:
        print("  Tareas configuradas:")
        for cod in tareas:
            config = cargar_casos(cod)
            print(f"    • {cod}  —  {config['total_casos']} casos  "
                  f"—  {config['puntaje_total']} pts en total")


def mostrar_resumen_casos(casos: list):
    """Muestra la tabla de casos ingresados hasta el momento."""
    if not casos:
        print("\n  (Aun no hay casos agregados)")
        return

    print()
    print(f"  {'#':<4} {'Entrada':<20} {'Esperado':<20} {'Puntaje':>8}")
    print("  " + "-" * 54)
    for caso in casos:
        print(f"  {caso['id']:<4} {caso['entrada']:<20} "
              f"{caso['esperado']:<20} {caso['puntaje']:>8.2f}")
    total = round(sum(c["puntaje"] for c in casos), 2)
    print("  " + "-" * 54)
    print(f"  {'':4} {'':20} {'TOTAL':>20} {total:>8.2f}")


# ── Funciones de entrada de datos ────────────────────────────

def pedir_cod_tarea() -> str:
    """
    Pide el código de la tarea.
    Convierte a mayúsculas y reemplaza espacios por guiones.
    Ejemplo: "tarea 1" → "TAREA-1"
    """
    print()
    print("  Ingresa el codigo de la tarea")
    print("  Ejemplo: TAREA-01, LABORATORIO-03, PARCIAL-1")
    while True:
        cod = input("  > ").strip().upper().replace(" ", "-")
        if cod:
            return cod
        print("  ⚠  El codigo no puede estar vacio.")


def pedir_id_profesor() -> str:
    """Pide el ID del profesor."""
    print()
    while True:
        id_prof = input("  Ingresa tu ID de profesor: ").strip()
        if id_prof:
            return id_prof
        print("  ⚠  El ID no puede estar vacio.")


def pedir_caso(numero: int) -> dict:
    """
    Guía al profesor para ingresar UN caso de prueba completo.

    Parámetros:
        numero (int): número del caso (para mostrarlo en pantalla)

    Retorna:
        dict con: id, entrada, esperado, puntaje
    """
    print()
    print(f"  ── Caso de prueba #{numero} ──────────────────────")

    # Entrada: lo que llegará al programa del estudiante
    print("  Entrada (lo que recibe el programa):")
    print("  Ejemplo: '2 3'  o  'hola mundo'  o  '10'")
    entrada = input("  > ").strip()

    # Salida esperada: lo que el programa debe imprimir
    print()
    print("  Salida esperada (lo que debe imprimir el programa):")
    print("  Ejemplo: '5'  o  'HOLA MUNDO'  o  'par'")
    esperado = input("  > ").strip()

    # Puntaje decimal: cuánto vale este caso
    print()
    print("  Puntaje de este caso (puede ser decimal, ej: 2.5):")
    while True:
        puntaje_str = input("  > ").strip().replace(",", ".")
        try:
            puntaje = float(puntaje_str)
            if puntaje <= 0:
                print("  ⚠  El puntaje debe ser mayor a 0.")
                continue
            break
        except ValueError:
            print("  ⚠  Escribe solo un numero. Ejemplos: 1  o  2.5  o  0.75")

    return {
        "id":       numero,
        "entrada":  entrada,
        "esperado": esperado,
        "puntaje":  round(puntaje, 2)
    }


def preguntar_agregar_otro() -> bool:
    """Pregunta si el profesor quiere agregar otro caso."""
    print()
    respuesta = input("  ¿Agregar otro caso de prueba? (s/n): ").strip().lower()
    return respuesta == "s"


def confirmar_guardado(cod_tarea: str, casos: list) -> bool:
    """
    Muestra el resumen final y pide confirmación antes de guardar.
    """
    print()
    print("=" * 56)
    print(f"  Resumen final para: {cod_tarea}")
    print("=" * 56)
    mostrar_resumen_casos(casos)
    print()
    respuesta = input("  ¿Confirmas y guardas esta configuracion? (s/n): ").strip().lower()
    return respuesta == "s"


def mostrar_exito_configuracion(config: dict):
    """Mensaje de éxito al guardar la configuración."""
    print()
    print("✅ " * 18)
    print()
    print("  CONFIGURACION GUARDADA EXITOSAMENTE")
    print()
    print(f"  Tarea          : {config['cod_tarea']}")
    print(f"  Casos creados  : {config['total_casos']}")
    print(f"  Puntaje total  : {config['puntaje_total']} pts")
    print(f"  Guardado en    : casos_de_prueba/{config['cod_tarea']}.json")
    print()
    print("✅ " * 18)


def mostrar_error(mensaje: str):
    print()
    print(f"  ❌ ERROR: {mensaje}")
    print()


# ── Flujo principal del panel del profesor ───────────────────

def ejecutar_panel_profesor():
    """
    Orquesta todo el flujo del panel del profesor.
    Es la función que llama main.py.
    """
    mostrar_encabezado_profesor()

    # Mostramos las tareas que ya existen
    mostrar_tareas_existentes()

    # Pedimos el ID y el código de tarea
    id_profesor = pedir_id_profesor()
    cod_tarea   = pedir_cod_tarea()

    # Verificamos si ya existe esa tarea
    existente = cargar_casos(cod_tarea)
    if existente:
        print()
        print(f"  ⚠  La tarea '{cod_tarea}' ya tiene {existente['total_casos']} casos configurados.")
        respuesta = input("  ¿Quieres sobreescribirla? (s/n): ").strip().lower()
        if respuesta != "s":
            print("  Operacion cancelada.")
            return

    # Bucle para agregar casos uno por uno
    casos = []
    print()
    print("  Ahora ingresa los casos de prueba.")
    print("  Por cada caso defines: entrada, salida esperada y puntaje.")

    while True:
        caso = pedir_caso(len(casos) + 1)
        casos.append(caso)

        # Mostramos la tabla actualizada después de cada caso
        print()
        print("  Casos ingresados hasta ahora:")
        mostrar_resumen_casos(casos)

        if not preguntar_agregar_otro():
            break

    # Confirmación final antes de guardar
    if not casos:
        mostrar_error("No ingresaste ningun caso. No se guardo nada.")
        return

    if confirmar_guardado(cod_tarea, casos):
        config = guardar_casos(cod_tarea, id_profesor, casos)
        mostrar_exito_configuracion(config)
    else:
        print()
        print("  Configuracion descartada. No se guardo nada.")