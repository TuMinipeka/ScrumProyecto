# =============================================================
# grader_ui.py
# Modulo — Interfaz de resultados de calificacion
# =============================================================
# Responsabilidad: mostrar al estudiante el resultado detallado
# de cada caso de prueba de forma clara y legible.
# =============================================================
# -*- coding: utf-8 -*-


def pedir_cod_tarea() -> str:
    """Pide al estudiante el codigo de la tarea a calificar."""
    print()
    print("  Para que tarea quieres calificar tu archivo?")
    print("  Ejemplo: TAREA-01, LABORATORIO-03")
    while True:
        cod = input("  > ").strip().upper().replace(" ", "-")
        if cod:
            return cod
        print("  El codigo no puede estar vacio.")


def mostrar_resultados(calificacion: dict):
    """
    Muestra el resultado completo de la calificacion.
    Disenado para que el estudiante entienda exactamente
    que paso en cada caso de prueba.
    """
    # Encabezado
    print()
    print("=" * 60)
    print("  RESULTADO DE CALIFICACION")
    print("=" * 60)
    print(f"  Tarea    : {calificacion['cod_tarea']}")
    print(f"  Archivo  : {calificacion['nombre_archivo']}")
    print()

    # Detalle caso por caso
    for r in calificacion["resultados"]:
        icono = "[OK]" if r["paso"] else "[FALLO]"
        print(f"  {icono} Caso #{r['caso_id']}  "
        f"[{r['puntaje_obtenido']:.2f} / {r['puntaje_posible']:.2f} pts]")
        print(f"     Entrada  : {r['entrada']}")
        print(f"     Esperado : {r['esperado']}")
        print(f"     Obtenido : {r['obtenido'] if r['obtenido'] else '(sin salida)'}")

        # Si hubo error mostramos el mensaje para que pueda corregirlo
        if r["error"]:
            print(f"     ERROR    : {r['error'][:80]}")
        if r["timeout"]:
            print("     TIEMPO   : Tu programa tardo demasiado (posible bucle infinito)")
        print()

    # Nota final
    print("-" * 60)
    nota    = calificacion["nota_obtenida"]
    maxima  = calificacion["nota_maxima"]
    porcent = calificacion["porcentaje"]

    # Barra visual de progreso con caracteres simples
    bloques_llenos = int(porcent / 5)    # 20 bloques = 100%
    barra = "#" * bloques_llenos + "-" * (20 - bloques_llenos)

    print(f"  NOTA FINAL : {nota:.2f} / {maxima:.2f} pts  ({porcent}%)")
    print(f"  [{barra}]")
    print()

    # Mensaje segun el resultado
    if porcent == 100:
        print("  Perfecto! Todos los casos pasaron.")
    elif porcent >= 60:
        print("  Buen trabajo. Revisa los casos que fallaron y vuelve a intentarlo.")
    else:
        print("  Sigue intentando. Revisa los errores arriba para corregir tu codigo.")
    print("=" * 60)