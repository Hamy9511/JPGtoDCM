from tkinter import *
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import filedialog

# Configuración de la ventana
root = ctk.CTk()
root.config(borderwidth=10)
root.title("JPGtoDICOM Sender")
root.geometry("400x900")
root.resizable(0, 0)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Configuración de grid
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)

# Variables globales
loaded_images = []
current_image_index = 0

# Funciones
def open_image():
    global current_image_index
    file_paths = filedialog.askopenfilenames(filetypes=[("JPG files", "*.jpg"), ("JPEG files", "*.jpeg"), ("All files", "*.*")])
    for file_path in file_paths:
        if file_path:
            image = Image.open(file_path)
            ctk_image = ctk.CTkImage(light_image=image, size=(400, 400))
            loaded_images.append(ctk_image)
    
    if len(loaded_images) > 0:
        current_image_index = 0
        update_image()
        if len(loaded_images) > 1:
            slider.configure(from_=0, to=len(loaded_images) - 1, state=NORMAL)  # Configurar el rango del slider
        else:
            slider.configure(state=DISABLED)  # Deshabilitar el slider si solo hay una imagen
        slider.set(0)  # Restablecer el slider a la posición inicial
    else:
        lPicture.configure(image=None, text="Sin Imagen")

def update_image():
    if loaded_images:
        ctk_image = loaded_images[current_image_index]
        lPicture.configure(image=ctk_image, text="")
        lPicture.image = ctk_image

def on_slider_change(value): 
        global current_image_index
        current_image_index = int(value)
        update_image()

def delete_List():
    global loaded_images
    loaded_images = []
    print("DATOS BORRADOS", len(loaded_images))

def push_uploadbutton():
    delete_List()
    open_image()



# Configuración de labels de datos del paciente
fInfo = ctk.CTkFrame(root, corner_radius=10)
fInfo.grid(row=0, column=0, rowspan=1, columnspan=2, sticky="nsew", padx=20, pady=20)
lInfo = ctk.CTkLabel(master=fInfo, text="INGRESAR DATOS DEL PACIENTE", font=("arial", 14))
lInfo.pack()

fId = ctk.CTkFrame(master=root, corner_radius=10)
fId.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
lId = ctk.CTkLabel(master=fId, text="ID del paciente:", font=("arial", 12))
lId.pack()

fName = ctk.CTkFrame(master=root, corner_radius=10)
fName.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
lName = ctk.CTkLabel(master=fName, text="Nombre:", font=("arial", 12))
lName.pack()

fLastname = ctk.CTkFrame(master=root, corner_radius=10)
fLastname.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")
lLastname = ctk.CTkLabel(master=fLastname, text="Apellido:", font=("arial", 12))
lLastname.pack()

fDate = ctk.CTkFrame(master=root, corner_radius=10)
fDate.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")
lDate = ctk.CTkLabel(master=fDate, text="Fecha del Examen:", font=("arial", 12))
lDate.pack()

# Configuración de textboxes
fEntryId = ctk.CTkFrame(root)
fEntryId.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
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

# Visor de las imágenes cargadas
fPicture = ctk.CTkFrame(root, corner_radius=10)
fPicture.grid(row=5, column=0, rowspan=1, columnspan=2, sticky="nsew", padx=20, pady=20)
lPicture = ctk.CTkLabel(master=fPicture, text="Sin Imagen")
lPicture.pack(fill=BOTH)

# Botones
bgRoot = root.cget("bg")
fButton = ctk.CTkFrame(root, fg_color=bgRoot)
fButton.grid(row=7, column=0, rowspan=1, columnspan=2, padx=10, pady=10, sticky="n")
BLoadImage = ctk.CTkButton(master=fButton, text="Cargar JPG", command=push_uploadbutton)
BSendImage = ctk.CTkButton(master=fButton, text="Enviar DCM")
BLoadImage.grid(row=0, column=0, padx=20)
BSendImage.grid(row=0, column=1, padx=20)

# Slider para ver imágenes
slider = ctk.CTkSlider(master=root, from_=0, to=100, command=on_slider_change, state=DISABLED)
slider.grid(row=6, column=0, rowspan=1, columnspan=2, sticky="nsew", padx=20, pady=20)

root.mainloop()  # Fin de la aplicación
