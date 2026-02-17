import csv
import json
import os

def guardar_txt():
    print ("\n----Guardar Datos En TXT----")
        
    nombre = input("Registre Su Nombre: ").capitalize()
    celular = input("Registre Su Numero De Celular: ")
    email = input("Ingrese su Email:")

    contacto = f"{nombre},{celular},{email}\n"
# "a" Se usa para almacenar varios Datos y no se borren
    with open("contactos.txt", "a") as archivo:
        archivo.write(contacto)
        print("Mensaje Guardado En TXT")

def guardar_csv():
    print("\n----Guardar Datos En CSV----")
    nombre = input("Registre Su Nombre: ").capitalize()
    celular = input("Registre Su Numero De Celular: ")
    email = input("Ingrese su Email:")

    with open("archivo.csv", "a", newline = "") as archivo:
        guardado = csv.writer(archivo)
        guardado.writerow([nombre,celular,email])
    print("Contacto Guardado En CSV")

def guardar_json():
    print("\n----Guardar Datos En JSON----")
    nombre = input("Registre Su Nombre: ").capitalize()
    celular = input("Registre Su Numero De Celular: ")
    email = input("Ingrese su Email:")

    datos = [
        {"nombre": nombre, "telefono": celular, "email": email},
    ]
    with open("datos.json", "a" ) as archivo:
        json.dump(datos,archivo, indent=4)
    print ("Contacto Guardado")

def leer_archivos():
    print("\n----Leyendo Contenido----")
    print("\n  Contenido TXT")
    if os.path.exists("contactos.txt"):
        with open("contactos.txt", "r") as archivo:
            contenido = archivo.read()
            print(contenido)
    else:
        print("El Archivo Aun No Existe")
    print("\n ---Contenido CSV---")
    if os.path.exists ("archivo.csv"):
        with open("archivo.csv","r")as archivo:
            lector = csv.reader(archivo)
            for fila in lector:
                print (fila)
    else:
        print("El Archivo Aun No Existe")
    print ("---Contenido JSON---")
    if os.path.exists ("datos.json"):
        with open("datos.json","r") as archivo:
            datos_json = json.load(archivo)
            print(datos_json)
    else:
        print("Archivo Aun No Existe")

def menu():
    while True:
        print("\n---GESTOR DE ARCHIVOS---")
        print("1. Guardar contacto en TXT")
        print("2. Guardar lista de contactos en CSV")
        print("3. Guarda diccionario De Contactos en JSON")
        print("4. Leer y mostrar Sus Contactos registrados")
        print("0. Salir")

        opcion = int(input("Selecione una opcion: "))
        if opcion==1:
            guardar_txt()
        elif opcion ==2:
            guardar_csv()
        elif opcion ==3:
            guardar_json()
        elif opcion==4:
            leer_archivos()
        elif opcion ==0:
            print("Saliendo Del PROGRAMA")
            break
        else:
            print("Opcion No Valida. Intente de nuevo")
menu()