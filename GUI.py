#Librerias
from tkinter import *
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import filedialog
import pydicom
from pydicom.dataset import FileDataset, Dataset
from pydicom.uid import generate_uid
from datetime import datetime


#Configuración de la ventana
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

#Listas
loaded_images = []

#Contador
current_image_index = 0

# Eventos

#Seleccion de imagenes
def open_image():
    global current_image_index
    file_paths = filedialog.askopenfilenames(filetypes=[("JPG files", "*.jpg"), ("JPEG files", "*.jpeg"), ("All files", "*.*")])
    if file_paths: 
        for file_path in file_paths: 
                image = Image.open(file_path)
                ctk_image = ctk.CTkImage(light_image=image, size=(400, 400)) 
                loaded_images.append(ctk_image)
        #Actualizar label de fecha
        entryDate.delete(0, END)
        entryDate.insert(0, get_current_date())
    #Comportamiento de label y slide
    if len(loaded_images) > 0:
        current_image_index = 0
        update_image()
        if len(loaded_images) > 1:
            slider.configure(from_=0, to=len(loaded_images) - 1, state=NORMAL)
            slider.set(0)
        else:
            slider.configure(state=DISABLED)
            slider.set(0)
    else:
        slider.configure(state=DISABLED)
        slider.set(0)
#adquirir fecha actual
def get_current_date():
    now = datetime.now()  # Usa datetime desde la biblioteca estándar
    return now.strftime("%d/%m/%Y")
#Actualiza las imagenes en el label
def update_image():
    global current_image_index
    if loaded_images:
        ctk_image = loaded_images[current_image_index]
        lPicture.configure(image=ctk_image, text="")
        lPicture.image = ctk_image
#Actualiza el slider
def on_slider_change(value):
        global current_image_index
        current_image_index = int(value)
        update_image()
#Reiniciar lista de imagenes
def delete_list():
    global loaded_images
    loaded_images.clear()
    print("DATOS BORRADOS", len(loaded_images))
#Comandos combinados
def push_uploadbutton():
    global loaded_images
    # Borra el contenido de los Entry
    entryId.delete(0, 'end')
    entryName.delete(0, 'end')
    entryLastname.delete(0, 'end')
    entryDate.delete(0, 'end')
    
    # Borra la lista de imágenes cargadas
    delete_list()
    open_image()

def push_sendbutton():
    if loaded_images:
        # Obtener datos del paciente
        patient_id = entryId.get()
        patient_name = entryName.get()
        exam_date_str = entryDate.get()
        # Validar y convertir la fecha
        try:
            exam_date = datetime.strptime(exam_date_str, '%d/%m/%Y')
        except ValueError:
            # Manejar el caso donde la fecha no coincide con el formato esperado
            print(f"Error: '{exam_date_str}' no es una fecha válida en formato DD-MM-YYYY.")
            return    
        # Inicializar series_number para la primera serie
        series_number = 1
        # Convertir cada imagen cargada a DICOM
        for i, ctk_image in enumerate(loaded_images, start=1):
            # Obtener la imagen original de CTkImage
            try:
                original_image = ctk_image._light_image  # Revisar si el atributo es _light_image
            except AttributeError:
                print("El objeto CTkImage no tiene un atributo _light_image.")
                return
            
            # Calcular instance_number para este frame
            instance_number = i
            
            # Convertir la imagen original a formato DICOM
            dicom_filename = convert_to_dicom(original_image, patient_id, patient_name, exam_date, series_number, instance_number)
            print(f"Imagen convertida a DICOM: {dicom_filename}")

def convert_to_dicom(image, patient_id, patient_name, exam_date, series_number, instance_number):
    # Crear un objeto Dataset DICOM vacío
    ds = Dataset()
    # Añadir metadatos DICOM requeridos
    ds.PatientID = patient_id
    ds.PatientName = patient_name
    ds.Modality = "OT"  # Modality (Modalidad) específica para tu tipo de imagen
    ds.StudyDate = exam_date.strftime('%Y%m%d') 
    # Obtener la hora actual
    current_time = datetime.now().strftime('%H%M%S')
    ds.StudyTime = current_time  
    ds.StudyInstanceUID = generate_uid()  # UID único para el estudio
    ds.SeriesInstanceUID = generate_uid()  # UID único para la serie
    ds.SOPInstanceUID = generate_uid()  # UID único para la instancia de imagen
    ds.SOPClassUID = '1.2.840.10008.5.1.4.1.1.481.2'  # Secondary Capture Image Storage
    # Añadir atributos específicos de la imagen
    ds.Rows, ds.Columns = image.size[1], image.size[0]
    ds.BitsAllocated = 8
    ds.BitsStored = 8
    ds.HighBit = 7
    ds.PixelRepresentation = 0
    ds.SamplesPerPixel = 3  # 3 para imágenes en color RGB
    # Establecer los atributos necesarios para la escritura del archivo DICOM
    ds.is_little_endian = True
    ds.is_implicit_VR = True
    # Convertir la imagen PIL a píxeles RGB y asignarla al dataset
    if image.mode != 'RGB':
        image = image.convert('RGB')  # Convertir a RGB si no lo es
    ds.PhotometricInterpretation = "RGB"
    ds.PixelData = image.tobytes()
    # Añadir más atributos para la serie y el frame
    ds.SeriesNumber = str(series_number)
    ds.InstanceNumber = str(instance_number)
    # Guardar el dataset como un archivo DICOM
    dicom_filename = f"{patient_id}_{exam_date.strftime('%Y%m%d_%H%M%S')}_{series_number}_{instance_number}.dcm"
    ds.save_as(dicom_filename)
    return dicom_filename

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

# Configuración de comboboxes
fEntryId = ctk.CTkFrame(root)
fEntryId.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
entryId = ctk.CTkEntry(master=fEntryId, justify=CENTER)
entryId.pack(fill=X)

fEntryName = ctk.CTkFrame(root)
fEntryName.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
entryName = ctk.CTkEntry(master=fEntryName, justify=CENTER)
entryName.pack(fill=X)

fEntryLastname = ctk.CTkFrame(root)
fEntryLastname.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
entryLastname = ctk.CTkEntry(master=fEntryLastname, justify=CENTER)
entryLastname.pack(fill=X)

fEntryDate = ctk.CTkFrame(root)
fEntryDate.grid(row=4, column=1, padx=10, pady=10, sticky="nsew")
entryDate = ctk.CTkEntry(master=fEntryDate, justify=CENTER)
entryDate.insert(0, get_current_date())
entryDate.configure(state="readonly")
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
BSendImage = ctk.CTkButton(master=fButton, text="Enviar DCM", command=push_sendbutton)
BLoadImage.grid(row=0, column=0, padx=20)
BSendImage.grid(row=0, column=1, padx=20)

# Slider para ver imágenes
slider = ctk.CTkSlider(master=root, from_=0, to=100, command=on_slider_change, state=DISABLED)
slider.grid(row=6, column=0, rowspan=1, columnspan=2, sticky="nsew", padx=20, pady=20)

# Fin de la aplicación
root.mainloop()  
