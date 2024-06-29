#import tkinter as tk #Libreria para interfaz, si uso estilos default
from tkinter import * #Agregando libreria tkinter
import customtkinter as ctk #Para estilo de interfaz
from PIL import Image, ImageTk
from tkinter import filedialog

#CONFIGURACION DE VENTANA

#root = tk.Tk() #Crear ventana con nombre Tkinter
root = ctk.CTk() #Ahora en vez de poner button = tk.button sera ctk.CTKButton
root.config(borderwidth=10) #Configuracion de estilos de la ventana
root.title("JPGtoDICOM Sender") #Titulo de la ventana
root.geometry("400x900") #Dimensiones de la ventana
root.resizable(0,0) #Configurando si o no se puede redimencionar la ventana 0 = false, 1 = True (width, height)
ctk.set_appearance_mode("dark") #Modo oscuro
ctk.set_default_color_theme("blue") #Color de los botones y widgets

#CONFIGURACION DE GRID
root.columnconfigure(0,weight=1) #Configuracionde columnas tipo grid (index,weight)
root.columnconfigure(1,weight=3)
#root.rowconfigure() #Configuración de filas tipo grid (index,weight)

#FUNCIONES DE LOS BOTONES

#Para abrir el explorador y buscar solo imagenes jpg

loadedImages =[] #Lista para cargar imagenes
def open_image():
    file_paths = filedialog.askopenfilename(filetypes=[("JPG files", "*.jpg"), ("JPEG files", "*.jpeg"), ("All files", "*.*")])
    
    for file_path in file_paths:
        if file_path:
            image = Image.open(file_path)
            ctk_image = ctk.CTkImage(light_image=image, size=(400, 400))
            loadedImages.append(ctk_image)

            # Actualizar el label con la nueva imagen
            lPicture.configure(image=ctk_image, text="")
            lPicture.image = ctk_image


#CONFIGURACION DE LABELS DE DATOS DEL PACIENTE

#Titulo
fInfo =ctk.CTkFrame(root, corner_radius=10) #Creación de un cajon
fInfo.grid(row=0, column=0, rowspan=1, columnspan=2, sticky="nsew", padx=20, pady=20) #Asignar y configurar celda del grid
lInfo = ctk.CTkLabel(master=fInfo, text="INGRESAR DATOS DEL PACIENTE", font=("arial", 14)) #Label asignado al frame
#lDatos.config(font=("arial", 14, "bold italic")) <-------------- Otra forma de agregar cambios al frame, label, etc.
lInfo.pack() #Ejecutando el label

#ID
fId =ctk.CTkFrame(master=root, corner_radius=10)
fId.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
lId = ctk.CTkLabel(master=fId, text="ID del paciente:", font=("arial", 12))
lId.pack()

#Nombre
fName =ctk.CTkFrame(master=root, corner_radius=10)
fName.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
lName = ctk.CTkLabel(master=fName, text="Nombre:", font=("arial", 12))
lName.pack()

#Apellido
fLastname =ctk.CTkFrame(master=root, corner_radius=10)
fLastname.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")
lLastname = ctk.CTkLabel(master=fLastname, text="Apellido:", font=("arial", 12))
lLastname.pack()

#Fecha
fDate =ctk.CTkFrame(master=root, corner_radius=10)
fDate.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")
lDate = ctk.CTkLabel(master=fDate, text="Fecha del Examen:", font=("arial", 12))
lDate.pack()

#CONFIGURACION DE TEXTBOX

fEntryId = ctk.CTkFrame(root)
fEntryId.grid(row=1, column=1, padx=10, pady=10, sticky="nsew") #combinando sticky="nsew" y .pack(fill=X) rellenamos toda la celda con el widget de vcombobox
entryId = ctk.CTkEntry(master=fEntryId)
entryId.pack(fill=X)

fEntryName = ctk.CTkFrame(root)
fEntryName.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
entryName = ctk.CTkEntry(master=fEntryName)
entryName.pack(fill=X)

fEntryLastname = ctk.CTkFrame(root)
fEntryLastname.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
entryLastname = ctk.CTkEntry(master=fEntryLastname)
entryLastname.pack(fill=X)

fEntryDate = ctk.CTkFrame(root)
fEntryDate.grid(row=4, column=1, padx=10, pady=10, sticky="nsew")
entryDate = ctk.CTkEntry(master=fEntryDate)
entryDate.pack(fill=X)

#VISOR DE LAS IMAGENES CARGADAS

fPicture = ctk.CTkFrame(root, corner_radius=10)
fPicture.grid(row=5, column=0, rowspan=1, columnspan=2, sticky="nsew", padx=20, pady=20)
lPicture = ctk.CTkLabel(master=fPicture, text="Sin Imagen")
lPicture.pack(fill=BOTH)

#BOTONES
bgRoot = root.cget("bg") #Para adquirir el color de la ventana
fButton = ctk.CTkFrame(root, fg_color=bgRoot)
fButton.grid(row=7, column=0, rowspan=1, columnspan=2, padx=10, pady=10, sticky="n")
BLoadImage = ctk.CTkButton(master=fButton, text="Cargar JPG", command=open_image)
BSendImage = ctk.CTkButton(master=fButton, text="Enviar DCM")
BLoadImage.grid(row=0, column=0, padx=20)
BSendImage.grid(row=0, column=1, padx=20)


#SLIDER PARA VER IMAGENES 

slider = ctk.CTkSlider(master=root, from_=0, to=100, border_width=10)
slider.grid(row=6, column=0, rowspan=1, columnspan=2, sticky="nsew", padx=20, pady=20)


root.mainloop() #Fin de app