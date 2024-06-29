#import tkinter as tk #Libreria para interfaz, si uso estilos default
from tkinter import * #Agregando libreria tkinter
import customtkinter #Para estilo de interfaz

#CONFIGURACION DE VENTANA
#window = tk.Tk() #Crear ventana con nombre Tkinter
window = customtkinter.CTk() #Ahora en vez de poner button = tk.button sera customtkinter.CTKButton
window.config(borderwidth=10) #Configuracion de estilos de la ventana
window.title("JPGtoDICOM Sender") #Titulo de la ventana
window.geometry("400x700") #Dimensiones de la ventana
window.resizable(0,0) #Configurando si o no se puede redimencionar la ventana 0 = false, 1 = True (width, height)

#CONFIGURACION DE GRID
window.columnconfigure(0,weight=1) #Configuracionde columnas tipo grid (index,weight)
window.columnconfigure(1,weight=3)
#window.rowconfigure() #Configuración de filas tipo grid (index,weight)

#CONFIGURACION DE LABELS DE DATOS DEL PACIENTE

#Titulo
fInput =customtkinter.CTkFrame(window, corner_radius=10) #Creación de un cajon
fInput.grid(row=0, column=0, rowspan=1, columnspan=2, sticky="nsew", padx=20, pady=20,) #Asignar y configurar celda del grid
lInput = customtkinter.CTkLabel(master=fInput, text="INGRESAR DATOS DEL PACIENTE", font=("arial", 14)) #Label asignado al frame
#lInput.config(font=("arial", 14, "bold italic")) <-------------- Otra forma de agregar cambios al frame, label, etc.
lInput.pack() #Ejecutando el label

#ID
fId =customtkinter.CTkFrame(master=window, corner_radius=10)
fId.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
lId = customtkinter.CTkLabel(master=fId, text="ID del paciente:", font=("arial", 12))
lId.pack()

#Nombre
fName =customtkinter.CTkFrame(master=window, corner_radius=10)
fName.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
lName = customtkinter.CTkLabel(master=fName, text="Nombre:", font=("arial", 12))
lName.pack()

#Apellido
fLastname =customtkinter.CTkFrame(master=window, corner_radius=10)
fLastname.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")
lLastname = customtkinter.CTkLabel(master=fLastname, text="Apellido:", font=("arial", 12))
lLastname.pack()

#Fecha
fDate =customtkinter.CTkFrame(master=window, corner_radius=10)
fDate.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")
lDate = customtkinter.CTkLabel(master=fDate, text="Fecha del Examen:", font=("arial", 12))
lDate.pack()

#CONFIGURACION DE TEXTBOX

fEntryId = customtkinter.CTkFrame(window)
fEntryId.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
entryId = customtkinter.CTkEntry(master=fEntryId)
entryId.pack(fill=X)

fEntryName = customtkinter.CTkFrame(window)
fEntryName.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
entryName = customtkinter.CTkEntry(master=fEntryName)
entryName.pack(fill=X)

fEntryLastname = customtkinter.CTkFrame(window)
fEntryLastname.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
entryLastname = customtkinter.CTkEntry(master=fEntryLastname)
entryLastname.pack(fill=X)

fEntryDate = customtkinter.CTkFrame(window)
fEntryDate.grid(row=4, column=1, padx=10, pady=10, sticky="nsew")
entryDate = customtkinter.CTkEntry(master=fEntryDate)
entryDate.pack(fill=X)

window.mainloop() #Fin de app