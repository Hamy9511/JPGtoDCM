import sys
sys.path.append("./Funciones")
import customtkinter as ctk
from tkinter import *
from datetime import datetime

# Configuración de la ventana
root = ctk.CTk()
root.config(borderwidth=10)
root.title("JPGtoDCM Sender")
root.geometry("1280x500")
root.resizable(0, 0)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Adquirir fecha actual
def get_current_date():
    now = datetime.now()
    return now.strftime("%d/%m/%Y")

# Comando de validación para aceptar solo números y limitar rango
def validate_numeric_input(value_if_allowed, min_val, max_val):
    if value_if_allowed == "":
        return True
    if value_if_allowed.isdigit():
        value = int(value_if_allowed)
        return min_val <= value <= max_val
    return False

# Comando de validación para year
def validate_year_input(value_if_allowed, length):
    if value_if_allowed == "":
        return True
    if value_if_allowed.isdigit() and len(value_if_allowed) <= length:
        return True
    return False

# Configuración de labels de datos del paciente
# Titulo
fInfo = ctk.CTkFrame(root, corner_radius=10)
fInfo.grid(row=0, column=0, rowspan=1, columnspan=4, sticky="nsew", padx=10, pady=10)
lInfo = ctk.CTkLabel(master=fInfo, text="INGRESAR DATOS DEL PACIENTE", font=("Helvetica", 18, "italic"))
lInfo.pack()

# Cajon de la info del paciente
bgRoot = root.cget("bg")
fPatientData = ctk.CTkFrame(root, fg_color=bgRoot)
fPatientData.grid(row=1, column=0, columnspan=4, padx=20, pady=20, sticky="nsew")
fPatientData.columnconfigure(0, weight=1)
fPatientData.columnconfigure(1, weight=3)
fPatientData.columnconfigure(2, weight=1)
fPatientData.columnconfigure(3, weight=3)

# Id
fId = ctk.CTkFrame(master=fPatientData, corner_radius=10)
fId.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
lId = ctk.CTkLabel(master=fId, text="ID del paciente:", font=("Helvetica", 14))
lId.pack()

# Nombre
fName = ctk.CTkFrame(master=fPatientData, corner_radius=10)
fName.grid(row=0, column=2, padx=5, pady=10, sticky="nsew")
lName = ctk.CTkLabel(master=fName, text="Nombre:", font=("Helvetica", 14))
lName.pack()

# Apellido
fLastname = ctk.CTkFrame(master=fPatientData, corner_radius=10)
fLastname.grid(row=1, column=2, padx=5, pady=10, sticky="nsew")
lLastname = ctk.CTkLabel(master=fLastname, text="Apellido:", font=("Helvetica", 14))
lLastname.pack()

# Fecha
fDate = ctk.CTkFrame(master=fPatientData, corner_radius=10)
fDate.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
lDate = ctk.CTkLabel(master=fDate, text="Fecha del Examen:", font=("Helvetica", 14))
lDate.pack()

# Fecha de nacimiento
fBirthday = ctk.CTkFrame(master=fPatientData, corner_radius=10)
fBirthday.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
lBirthday = ctk.CTkLabel(master=fBirthday, text="Fecha de nacimiento:", font=("Helvetica", 14))
lBirthday.pack()
fBirthdaySpace = ctk.CTkFrame(master=fPatientData, fg_color=bgRoot)
fBirthdaySpace.grid(row=2, column=1, padx=10, pady=10, sticky="w")

# Genero
fGender = ctk.CTkFrame(master=fPatientData, corner_radius=10)
fGender.grid(row=2, column=2, padx=5, pady=10, sticky="nsew")
lGender = ctk.CTkLabel(master=fGender, text="Genero:", font=("Helvetica", 14))
lGender.pack()

# Descripcion
fDescription = ctk.CTkFrame(master=fPatientData, corner_radius=10)
fDescription.grid(row=3, column=0, padx=5, pady=10, sticky="we")
lDescription = ctk.CTkLabel(master=fDescription, text="Descripción:", font=("Helvetica", 14))
lDescription.pack(fill=Y)

# Contador de Frames
lCount = ctk.CTkLabel(root, text="")
lCount.grid(row=0, column=5, sticky="s")

# Configuración de entradas de datos
entryId = ctk.CTkEntry(master=fPatientData, justify=CENTER, font=("Helvetica", 14), width=200, state="readonly")
entryId.grid(row=0, column=1, padx=10, pady=10, sticky="w")

# Nombre
entryName = ctk.CTkEntry(master=fPatientData, justify=CENTER, font=("Helvetica", 14), width=200, state="readonly")
entryName.grid(row=0, column=3, padx=10, pady=10, sticky="w")

# Apellido
entryLastname = ctk.CTkEntry(master=fPatientData, justify=CENTER, font=("Helvetica", 14), width=200, state="readonly")
entryLastname.grid(row=1, column=3, padx=10, pady=10, sticky="w")

# Fecha
entryDate = ctk.CTkEntry(master=fPatientData, justify=CENTER, font=("Helvetica", 14))
entryDate.insert(0, get_current_date())
entryDate.configure(state="readonly")
entryDate.grid(row=1, column=1, padx=10, pady=10, sticky="w")

# Descripcion
textboxDescription = ctk.CTkEntry(fPatientData, font=("Helvetica", 14), state=DISABLED)
textboxDescription.grid(row=3, column=1, rowspan=1, columnspan=3, padx=10, pady=10, sticky="we")

# Genero
OptionMenuGender = ctk.CTkOptionMenu(master=fPatientData, values=["M", "F", "O"], width=70, state=DISABLED)
OptionMenuGender.set("")
OptionMenuGender.grid(row=2, column=3, padx=10, pady=10, sticky="w")

# Validar solo números y rango para entradas de día, mes y año
validate_day_command = root.register(lambda value: validate_numeric_input(value, 1, 31))
validate_month_command = root.register(lambda value: validate_numeric_input(value, 1, 12))
validate_year_command = root.register(lambda value: validate_year_input(value, 4))
# Fecha de nacimiento - Día
entryDay = ctk.CTkEntry(master=fBirthdaySpace, width=40, justify=CENTER, validate="key", validatecommand=(validate_day_command, "%P"), state=DISABLED)
entryDay.grid(row=0, column=0)

# Fecha de nacimiento - Mes
entryMonth = ctk.CTkEntry(master=fBirthdaySpace, width=40, justify=CENTER, validate="key", validatecommand=(validate_month_command, "%P"), state=DISABLED)
entryMonth.grid(row=0, column=2)

# Fecha de nacimiento - Año
entryYear = ctk.CTkEntry(master=fBirthdaySpace, width=50, justify=CENTER, validate="key", validatecommand=(validate_year_command, "%P"), state=DISABLED)
entryYear.grid(row=0, column=4)

# Separadores
lSeparador1 = ctk.CTkLabel(master=fBirthdaySpace, text="/", font=("Helvetica", 16))
lSeparador1.grid(row=0, column=1, padx=5)
lSeparador2 = ctk.CTkLabel(master=fBirthdaySpace, text="/", font=("Helvetica", 16))
lSeparador2.grid(row=0, column=3, padx=5)

# Visor de las imágenes cargadas
fPicture = ctk.CTkFrame(root, fg_color=bgRoot, corner_radius=10, width=400, height=400)
fPicture.grid(row=1, column=5, sticky="nsew", pady=20, padx=10)
fPicture.pack_propagate(FALSE)
lPicture = ctk.CTkLabel(master=fPicture, text="Sin Imagen")
lPicture.pack(expand=TRUE)

# Botones
fButton = ctk.CTkFrame(fPatientData, fg_color=bgRoot)
fButton.grid(row=4, column=1, columnspan=3, padx=10, pady=40, sticky="n")
BLoadImage = ctk.CTkButton(master=fButton, text="Cargar JPG") #pus_cargarbutton
BSendImage = ctk.CTkButton(master=fButton, text="Convertir a DCM") #push_convertbutton
BSend = ctk.CTkButton(master=fButton, text="Enviar Paciente") #send_button
BSend.grid(row=0, column=2, padx=20)
BLoadImage.grid(row=0, column=0, padx=20)
BSendImage.grid(row=0, column=1, padx=20)

# Slider para ver imágenes
slider = ctk.CTkSlider(master=root, from_=0, to=100, orientation=VERTICAL, state=DISABLED) #on__slider_change
slider.grid(row=1, column=4, rowspan=4, pady=40)

# Función para cerrar la ventana y detener todo
def on_closing():
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Fin de la aplicación
root.mainloop()
