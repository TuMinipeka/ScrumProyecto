from logs import registrar_log
import json
import os
admin_contra = "0320"
usuario_actual = {"tipo": "Residente"}


def gestion_usuarios ():
    global usuario_actual
    print("\n<<<<<<-SISTEMA COMUNITARIO->>>>>>")
    print("        Bienvenido Vecino")
    try:
        name  = input("Ingrese Su Nombre Vecino: ").capitalize()
        id_veci = input(f"Ingrese Su ID {name} : ")
        apellido = input(f"Ingrese su apellido {name } : ").capitalize()
        telefono = input(f"Ingrese Su Numero de Telefono {name} {apellido} : ")
        direccion = input(f"Ingrese Su Direccion {name} : ")
        print("Que Tipo De Usuario Es Usted")
        print ("1. Administrador")
        print ("2. Residente")
        
        tipo_usuario = int(input("Ingresa Una Opcion: "))
        if tipo_usuario == 1:
            if not verificar_admin():
                print("No Se Pudo Activar El Modo Admin")
                return
            tipo_usuario_texto = "Administrador"
            usuario_actual["tipo"] = "Administrador"
            print("Modo Administrado Activado")
        elif tipo_usuario == 2:
            tipo_usuario_texto = "Residente"
            print("Modo Residente Activado")
        else:
            raise ValueError ("Opcion no valida")
        

        if not name or not telefono or not apellido or not direccion or not id_veci or not tipo_usuario or not tipo_usuario_texto:
            raise ValueError("Te falto llenar Datos")
    except KeyboardInterrupt:
            print("Proceso finalizado por el usuario.")
    except Exception:
            print("Ocurrio un error inesperado.") 
    diccionario = {
        "nombre": name,
        "apellido": apellido,
        "telefono": telefono,
        "direccion": direccion,
        "tipo_usuario": tipo_usuario_texto
    }
    usuario_actual["tipo"] = tipo_usuario_texto
    # Guardar Datos en Json
    try:
            datos_actuales = {}

            if os.path.exists("vecino.json"):
                with open("vecino.json","r",encoding="utf-8") as archivo_json:
                    datos_actuales = json.load(archivo_json)

                    if id_veci in datos_actuales:
                        print("Este ID ya esta registrado")
                        return
            datos_actuales[id_veci] = diccionario              

            with open("vecino.json","w",encoding="utf-8") as archivo_writer_json:
                json.dump(datos_actuales, archivo_writer_json, indent=4,ensure_ascii=False)
                        
                print("Vecino guardado exitosamente.")
    except PermissionError:
            print("No cuenta con los permisos necesarios para agregar contactos.")
    except Exception as e:
            print(f"Error inesperado en JSON: {e}")

    registrar_log(
        "INFO",
        f"Usuario {usuario_actual['tipo']} registró vecino {id_veci}"
    )

   # Funcion Para verificar contraseña
def verificar_admin():
    intentos=3
    while intentos > 0:
        password = input("Ingrese La Contraseña: ")
        if password == admin_contra:
            print("Acceco Administrador")
            return True
        else:
            intentos -=1
            print(f"Contraseña Incorrecta. Intentos restantes {intentos}")
    print("Se Agotaron Los Intentos. Acceso Denegado")
    return False
   # Leer Listas Vecinos
def listas_vecinos ():
    print("\n -----Listas De Vecinos-----")
    try:
        with open("vecino.json","r", encoding="utf-8") as archivo_json:
            datos = json.load(archivo_json)

        for id_veci, v in datos.items():
            print ("---------------------------------")
            print(f"ID: {id_veci} ")
            print(f"Nombre: {v['nombre']}")
            print(f"Apellido: {v['apellido']}")
            print(f"Telefono: {v['telefono']}")
            print(f"Dirección: {v['direccion']}")
            print(f"Tipo De Usuario: {v['tipo_usuario']}")
    except FileNotFoundError:
        print("Ningún Vecino Se Ha Registrado.")
#buscar id Vecino
def buscar_id():
    print("\n ===Buscar Vecino Por ID===")
    id_buscar=input("Ingrece el ID Del Vecino: ")
    try:
        with open("vecino.json","r",encoding="utf-8") as archivo:
            datos = json.load(archivo)
            if id_buscar in datos:
                v = datos[id_buscar]
                print("------ VECINO ENCONTRADO ------")
                print(f"Nombre: {v['nombre']}")
                print(f"Apellido: {v['apellido']}")
                print(f"Teléfono: {v['telefono']}")
                print(f"Dirección: {v['direccion']}")
                print(f"Tipo Usuario: {v['tipo_usuario']}")
            else:
                print("No existe un vecino con ese ID.")
    except FileNotFoundError:
        print("No hay vecinos registrados.")
        
# Actualizar Datos Vecinos
def actualizar_vecino():
    print("\n ===Actualizar Informacion===")
    id_buscar = input ("Ingrese el ID del vecino a actualizar: ")
    try:
        with open("vecino.json","r",encoding="utf-8") as archivo:
             datos=json.load(archivo)
        if id_buscar not in datos:
            return print("No existe algún vecino con ese ID")
        vecino = datos [id_buscar]
        print("\n (Enter Para Mantener El Dato Actual)")
        nuevo_nombre = input (f"Nombre [{vecino['nombre']}]:") or vecino["nombre"]
        nuevo_apellido = input (f"Apellido[{vecino['apellido']}]:") or vecino["apellido"]
        nuevo_telefono = input (f"Telefono[{vecino['telefono']}]:") or vecino["telefono"]
        nuevo_direccion = input (f"Direccion[{vecino['direccion']}]:") or vecino["direccion"]
        
        print("Tipo de usuario:")
        print("1. Administrador")
        print("2. Residente")
        opcion = input(f"Opción actual [{vecino['tipo_usuario']}]: ")

        if opcion == "1":
            nuevo_tipo = "Administrador"
        elif opcion == "2":
            nuevo_tipo = "Residente"
        else:
            nuevo_tipo = vecino["tipo_usuario"]

        datos[id_buscar] = {
            "nombre": nuevo_nombre,
            "apellido": nuevo_apellido,
            "telefono": nuevo_telefono,
            "direccion": nuevo_direccion,
            "tipo_usuario": nuevo_tipo
        }

        with open("vecino.json", "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
            print("-----Archivo actualizado correctamente-----")

    except FileNotFoundError:
        print("No hay vecinos registrados.")
    except Exception as e:
        print(f"Error al actualizar: {e}")
# Eliminar Datos Del Vecino
def eliminar():
    print("\n === Eliminar Vecino ===")
    id_buscar = input("Ingrese El ID Del Vecino Que Desea Eliminar: ")
    try:
        with open ("vecino.json", "r", encoding="utf-8") as f:
            datos=json.load(f)
        if id_buscar not in datos:
            print("No Hay Vecino Registrado Con Ese ID")
            return
        vecino= datos[id_buscar]
        print(f"Vecino: {vecino['nombre']} {vecino['apellido']}")

        confirmar = input ("Seguro Que Desea Eliminar Ese Vecino (si/no): ").lower()
        if confirmar !="si":
            print ("Cancelando Eliminacion")
            return
        del datos[id_buscar]
        with open("vecino.json", "w", encoding="utf-8") as arc:
            json.dump(datos, arc, indent=4, ensure_ascii=False)

        print(" Vecino Eliminado Exitosamente")
    except FileNotFoundError:
        print("No Hay Vecino Registrado")
    except Exception as e:
        print(f"Error inesperado al elimiar: {e}")

    registrar_log(
    "WARNING",
    f"Administrador eliminó vecino {id_buscar}"
    )
    registrar_log(
    "WARNING",
    "Residente intentó eliminar un vecino"
    )


# Menu De Opciones 
def menu_usuario(usuario_actual):
    while True:
        print("\n=====MENU COMUNIDAD=====")
        try:
            print("1. Registrar Vecino")
            print("2. Listar Vecinos")
            print("3. Buscar ID")
            print("4. Actualizar INFO")
            print("5. Eliminar Vecino")
            print("6. Salir")

            opcion= int(input("Ingrese Una Opcion: "))
            if opcion == 1:
                gestion_usuarios()
            elif opcion == 2:
                listas_vecinos()
            elif opcion == 3:
                buscar_id()
            elif opcion == 4:
                if usuario_actual["tipo"] == "Administrador":
                    actualizar_vecino()
                else:
                    print("Solo El Administrador Puede Hacer Estos Cambios.")
            elif opcion ==5:
                if usuario_actual["tipo"] != "Administrador":
                    eliminar()
                else:
                    print("Solo El Administrador Puede Hacer Estos Cambios.")
            elif opcion == 6:
                print("Saliendo del programa...")
                break
            else:
                    print("Opcion no valida. Intente nuevamente")
        except ValueError:
            print("La opcion debe ser un valor numerico.")
            continue
        except Exception as e:
            print(f"Ocurrio un error inesperado: {e}")
            break