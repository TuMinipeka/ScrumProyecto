import csv
import json
import os

def guardar_txt():
    print("\n---GUARDAR EN TXT---")
    mensaje = input("Ingrese el mensaje que desea guardar: ")

    with open("archivo_texto.txt","w") as archivo:
        archivo.write(mensaje)
    
    print("Mensaje guardado en el archivo TXT")

def guardar_csv():
    print("\n---GUARDAR EN CSV---")
    datos=[
        ["Nombre","Edad","Ciudad"],
        ["Camila","23","Bucaramanga"],
        ["Jose","18","Floridablanca"],
        ["Ana","25","Medellin"]
    ]

    with open("archivo_datos.csv","w",newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerows(datos)

    print("Datos guardado en archivo CSV")

def guardar_json():
    diccionario = {
        "producto":"Laptop",
        "precio":1200,
        "disponible":True,
        "especificaciones":{
            "ram":"16GB",
            "disco": "512GB SSD"
        }
    }

    with open("archivo_data.json","w") as archivo:
        json.dump(diccionario,archivo,indent=4)
    
    print("Diccionario guardado en el archivo JSON")

def leer_archivos():
    print("\n---LEYENDO CONTENIDOS---")

    print("\n1. Contenido de TXT")
    if os.path.exists("archivo_texto.txt"):
        with open("archivo_texto.txt","r") as archivo:
            contenido = archivo.read()
            print(contenido)
    else:
        print("El archivo TXT aun no existe.")

    print("\n---CONTENIDO CSV---")
    if os.path.exists("archivo_datos.csv"):
        with open("archivo_datos.csv", "r") as archivo:
            lector = csv.reader(archivo)
            for fila in lector:
                print(fila)
    else:
        print("El archivo CSV aun no existe.")

    print("\n---CONTENIDO JSON---")
    if os.path.exists("archivo_data.json"):
        with open("archivo_data.json","r") as archivo:
            datos_json = json.load(archivo)
            print(datos_json)
    else:
        print("El archivo JSON aun no existe.")

def menu():
    while True:
        print("\n---GESTOR DE ARCHIVOS---")
        print("1. Guardar contacto en TXT")
        print("2. Guardar lista de contactos en CSV")
        print("3. Guarda diccionario De Contactos en JSON")
        print("4. Leer y mostrar Sus Contactos registrados")
        print("0. Salir")

        opcion = int(input("Seleccione una opcion: "))

        if opcion == 1:
            guardar_txt()
        elif opcion == 2:
            guardar_csv()
        elif opcion == 3:
            guardar_json()
        elif opcion == 4:
            leer_archivos()
        elif opcion == 0:
            print("Saliendo del programa...")
            break
        else:
            print("Opcion no valida. Intene de nuevo")

menu()