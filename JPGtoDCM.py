# Librerias
import os
import tkinter as tk
import customtkinter as ctk
import pydicom
from datetime import datetime
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from pydicom.dataset import FileDataset, Dataset
from pydicom.uid import ExplicitVRLittleEndian, generate_uid, UID
from pydicom import config, dcmread
import uuid
from pynetdicom import AE, StoragePresentationContexts

# Directorio base donde se guardarán las carpetas de cada paciente 
base_directory = "./dicom_images"
base_directory1 = "./JPG_images"

# Crear directorio base si no existe
if not os.path.exists(base_directory):
    os.makedirs(base_directory)

if not os.path.exists(base_directory1):
    os.makedirs(base_directory1)
    
#Variables Globales
global_study_instance_uid = generate_uid()
global_series_instance_uid = generate_uid()

# Configuración de la ventana
root = ctk.CTk()
root.config(borderwidth=10)
root.title("JPGtoDCM Sender")
root.geometry("1280x500")
root.resizable(0, 0)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Configuración de grid
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)
root.columnconfigure(4, weight=1) 

# Listas
loaded_images = []

# Contador
current_image_index = 0


#FUNCIONES

# Adquirir fecha actual
def get_current_date():
    now = datetime.now()
    return now.strftime("%d/%m/%Y")

# Actualiza las imagenes en el label
def update_image():
    global current_image_index
    if loaded_images:
        ctk_image = loaded_images[current_image_index]
        lPicture.configure(image=ctk_image, text="")

# Actualiza el slider
def on_slider_change(value):
    global current_image_index
    current_image_index = int(value)
    update_image()

# Reiniciar lista de imagenes
def delete_list():
    global loaded_images
    loaded_images.clear()


# Comando de validación para aceptar solo números y limitar rango
def validate_year_input(value_if_allowed, length):
    if value_if_allowed == "":
        return True
    if value_if_allowed.isdigit() and len(value_if_allowed) <= length:
        return True
    return False

def validate_numeric_input(value_if_allowed, min_val, max_val):
    if value_if_allowed == "":
        return True
    if value_if_allowed.isdigit():
        value = int(value_if_allowed)
        return min_val <= value <= max_val
    return False

# Comportamiento del boton para cargar los JPG
def push_cargarbutton():
    global loaded_images

    # Borra el contenido de los Entry
    entryId.configure(state=NORMAL)
    entryName.configure(state=NORMAL)
    entryLastname.configure(state=NORMAL)
    entryDay.configure(state=NORMAL)
    entryMonth.configure(state=NORMAL)
    entryYear.configure(state=NORMAL)
    textboxDescription.configure(state=NORMAL)
    OptionMenuGender.configure(state=NORMAL)
    entryId.delete(0, 'end')
    entryName.delete(0, 'end')
    entryLastname.delete(0, 'end')
    entryDay.delete(0, 'end')
    entryMonth.delete(0, 'end')
    entryYear.delete(0, 'end')
    textboxDescription.delete(0, 'end')
    OptionMenuGender.set("")

    # Borra la lista de imágenes cargadas
    delete_list()
    open_image()

# Seleccion de imagenes
def open_image():
    global current_image_index
    global global_study_instance_uid, global_series_instance_uid

    # Generar nuevos UIDs para una nueva sesión de imágenes
    global_study_instance_uid = generate_uid()
    global_series_instance_uid = generate_uid()

    initial_folder = "./JPG_images"
    file_paths = filedialog.askopenfilenames(
        initialdir = initial_folder, 
        filetypes=[("JPG files", "*.jpg"), ("JPEG files", "*.jpeg"), ("All files", "*.*")],
        title="Seleccionar imágenes JPG/JPEG"
    )
    if file_paths:
        for file_path in file_paths:
            image = Image.open(file_path)
            
            #Ajustando dimensiones de la imagen en label
            max_width = 400
            max_height = 400
            width_image_original, height_image_orinal = image.size
            aspect_ratio = width_image_original/height_image_orinal
            if width_image_original > height_image_orinal:
                new_width = min(width_image_original, max_width)
                new_height = int(new_width/aspect_ratio)
            else:
                new_height = min(height_image_orinal, max_height)
                new_width = int(new_height*aspect_ratio)
            ctk_image = ctk.CTkImage(light_image=image, size=(new_width, new_height))
            loaded_images.append(ctk_image)
        # Actualizar label de fecha
        entryDate.delete(0, END)
        entryDate.insert(0, get_current_date())
    # Comportamiento de label y slide
    if len(loaded_images) > 0:
        current_image_index = 0
        update_image()
        if len(loaded_images) > 1:
            slider.configure(from_=0, to=len(loaded_images) - 1, state=NORMAL)
            slider.set(0)
            lCount.configure(text=f"FRAMES: {len(loaded_images)}", font=("Helvetica", 14, "italic"))
        else:
            slider.configure(state=DISABLED)
            slider.set(0)
            lCount.configure(text=f"FRAMES: {len(loaded_images)}", font=("Helvetica", 14, "italic"))
    else:
        slider.configure(state=DISABLED)
        slider.set(0)

#Comportamiento del boton para convertir a DCM
def push_convertbutton():
    global success
    success = False  # Inicializar success fuera del bloque if

    # Obtener datos del paciente
    patient_id = entryId.get().strip()
    patient_name = entryName.get().strip()
    lastname = entryLastname.get().strip()
    exam_date_str = entryDate.get().strip()
    gender = OptionMenuGender.get().strip()
    description = textboxDescription.get().strip()
    day = entryDay.get().strip()
    month = entryMonth.get().strip()
    year = entryYear.get().strip() 

    if len(day) == 1:
        day = f"0{day}"
    if len(month) == 1:
        month = f"0{month}"
    birthday = f"{year}{month}{day}"
    

    # Verificar si algún campo está vacío
    if not patient_id or not patient_name or not lastname or not exam_date_str:
        messagebox.showerror("Error", "Todos los campos de ID del paciente, Nombre, Apellido y Fecha del examen deben ser llenados.")
        return

    try:
        exam_date = datetime.strptime(exam_date_str, '%d/%m/%Y')
    except ValueError:
        # Manejar el caso donde la fecha no coincide con el formato esperado
        messagebox.showerror("Error", "La fecha del examen no es válida. Use el formato DD/MM/YYYY.")
        return
    try:
        Birthday = datetime.strptime(exam_date_str, '%d/%m/%Y')
    except ValueError:
        # Manejar el caso donde la fecha no coincide con el formato esperado
        messagebox.showerror("Error", "La fecha de nacimiento no es válida. Use el formato DD/MM/YYYY.")
        return

    if loaded_images:
        # Crear directorio para el paciente si no existe
        patient_directory = os.path.join(base_directory, f"Patient_{patient_id}_{patient_name}")
        if not os.path.exists(patient_directory):
            os.makedirs(patient_directory)

        # Inicializar series_number para la primera serie
        series_number = 1
        success = True  # Variable para rastrear el éxito de la conversión

        # Convertir cada imagen cargada a DICOM
        for i, ctk_image in enumerate(loaded_images, start=1):
            # Obtener la imagen original de CTkImage
            try:
                original_image = ctk_image._light_image  # Revisar si el atributo es _light_image
            except AttributeError:
                print("El objeto CTkImage no tiene un atributo _light_image.")
                success = False  # Marcar éxito como falso si alguna conversión falla
                break  # Detener el proceso de conversión si ocurre un error

            # Calcular instance_number para este frame
            instance_number = i

            # Convertir la imagen original a formato DICOM
            dicom_filename = convert_to_dicom(original_image, patient_id, patient_name, lastname, exam_date, gender, birthday, description, series_number, instance_number, patient_directory)
            if dicom_filename:
                print(f"Imagen convertida a DICOM: {dicom_filename}")
            else:
                success = False  # Marcar éxito como falso si alguna conversión falla
                break  # Detener el proceso de conversión si ocurre un error

        if success:
            messagebox.showinfo("Estado de conversión de imágenes", "Imágenes JPG convertidas a DICOM exitosamente")
        else:
            messagebox.showerror("Estado de conversión de imágenes", "Hubo un error al convertir algunas imágenes a DICOM")
    else:
        messagebox.showerror("Error", "No hay imágenes cargadas para convertir.")

# Converitr JPG a DCM
def convert_to_dicom(image, patient_id, patient_name, lastname, exam_date, birthday, gender, description, series_number, instance_number, patient_directory):
    global global_study_instance_uid, global_series_instance_uid

    image = image.convert("RGB")

    # Crear un objeto Dataset DICOM vacío
    file_meta = pydicom.dataset.FileMetaDataset()
    file_meta.MediaStorageSOPClassUID = pydicom.uid.SecondaryCaptureImageStorage
    file_meta.MediaStorageSOPInstanceUID = generate_uid()
    file_meta.ImplementationClassUID = generate_uid()

    ds = FileDataset("", {}, file_meta=file_meta, preamble=b"\0" * 128)

    # Añadir metadatos DICOM requeridos
    ds.PatientID = patient_id
    ds.PatientName = f"{lastname}^{patient_name}"
    ds.PatientBirthDate = gender
    ds.PatientSex = birthday
    ds.StudyDescription = description
    ds.StudyInstanceUID = global_study_instance_uid
    ds.SeriesInstanceUID = global_series_instance_uid
    ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
    ds.SOPClassUID = file_meta.MediaStorageSOPClassUID
    ds.ImageType = ["DERIVED", "SECONDARY", ""]
    ds.PhotometricInterpretation = "RGB"
    ds.SamplesPerPixel = 3
    ds.Rows, ds.Columns = image.size[1], image.size[0]
    ds.BitsAllocated = 8
    ds.BitsStored = 8
    ds.HighBit = 7
    ds.PixelRepresentation = 0
    ds.Modality = "DM"  # Modality Digital Microscopy
    # Convertir la imagen JPEG a píxeles y almacenarla como píxeles RGB
    ds.PixelData = image.tobytes()
    ds.StudyDate = exam_date.strftime('%Y%m%d')
    current_time = datetime.now().strftime('%H%M%S')
    ds.StudyTime = current_time
    ds.SeriesNumber = str(series_number)  # Convertir a cadena si es un número entero
    ds.InstanceNumber = str(instance_number)  # Convertir a cadena si es un número entero
    ds.is_little_endian = True
    ds.is_implicit_VR = True

    # Nombre de archivo DICOM
    dicom_filename = os.path.join(patient_directory, f"{patient_name}_{lastname}_{exam_date.strftime('%Y%m%d')}_S{series_number}_I{instance_number}.dcm")
    # Guardar el dataset como archivo DICOM
    ds.save_as(dicom_filename, write_like_original=False)
    return dicom_filename

#Comportamiento del boton Enviar Paciente
def send_button():
    global base_directory
    initial_dir = "./dicom_images"
    folder_path = filedialog.askdirectory(
        initialdir=initial_dir,
        title="Seleccionar Carpeta de Imágenes DICOM"
    )
    if folder_path:
        main(folder_path)  # Asegúrate de pasar folder_path a main()

#ENVIO AL PACS
def generate_dicom_uid():

    return UID(f"1.2.826.0.1.3680043.9.7237.{uuid.uuid4()}")

def ensure_valid_uids(ds):

    if 'StudyInstanceUID' not in ds or not ds.StudyInstanceUID.is_valid:
        ds.StudyInstanceUID = generate_dicom_uid()
    if 'SeriesInstanceUID' not in ds or not ds.SeriesInstanceUID.is_valid:
        ds.SeriesInstanceUID = generate_dicom_uid()
    if 'SOPInstanceUID' not in ds or not ds.SOPInstanceUID.is_valid:
        ds.SOPInstanceUID = generate_dicom_uid()

def send_to_pacs(dicom_file, pacs_ip, pacs_port):
    ae = AE()
    # Agregar contextos de presentación para almacenamiento de imágenes DICOM
    ae.add_requested_context(UID('1.2.840.10008.5.1.4.1.1.7'), ['1.2.840.10008.1.2'])  # Secondary Capture Image Storage
    try:
        ds = dcmread(dicom_file)
    except Exception as e:
        print(f"Error al leer {dicom_file}: {str(e)}")
        return False
    ensure_valid_uids(ds)
    assoc = ae.associate(pacs_ip, pacs_port)
    if assoc.is_established:
        status = assoc.send_c_store(ds)
        assoc.release()
        print(f"Enviado {dicom_file} al PACS con estado: {status}")
        return True
    else:
        print("Error: No se pudo establecer la asociación con el PACS.")
        return False

def main(folder_path):
    # Configuración del PACS
    pacs_ip = '192.168.2.101'  # IP del servidor PACS
    pacs_port = 4242  # Puerto del servidor PACS

    # Variable para controlar el estado del envío
    all_sent = True

    # Iterar sobre los archivos en la carpeta
    for filename in os.listdir(folder_path):
        if filename.endswith('.dcm'):  # Asumiendo que son archivos DICOM
            file_path = os.path.join(folder_path, filename)
            if not send_to_pacs(file_path, pacs_ip, pacs_port):
                all_sent = False
                break  # Detener el bucle al primer error

    if all_sent:
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Éxito", "Todos los archivos DICOM se enviaron exitosamente al PACS.")
    else:
        root = tk.Tk()
        root.withdraw()
        messagebox.showwarning("Advertencia", "Algunos archivos DICOM no se pudieron enviar al PACS.")

# Configuración de labels de datos del paciente
fInfo = ctk.CTkFrame(root, corner_radius=10)
fInfo.grid(row=0, column=0, rowspan=1, columnspan=4, sticky="nsew", padx=10, pady=10)
lInfo = ctk.CTkLabel(master=fInfo,text="INGRESAR DATOS DEL PACIENTE",font=("Helvetica",18,"italic"))
lInfo.pack()

bgRoot = root.cget("bg")
fPatientData = ctk.CTkFrame(root, fg_color=bgRoot)
fPatientData.grid(row=1, column=0, columnspan=4, padx=20, pady=20, sticky="nsew")
fPatientData.columnconfigure(0,weight=1)
fPatientData.columnconfigure(1,weight=3)
fPatientData.columnconfigure(2,weight=1)
fPatientData.columnconfigure(3,weight=3)

fId = ctk.CTkFrame(master=fPatientData, corner_radius=10)
fId.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
lId = ctk.CTkLabel(master=fId, text="ID del paciente:", font=("Helvetica", 14))
lId.pack()

fName = ctk.CTkFrame(master=fPatientData, corner_radius=10)
fName.grid(row=0, column=2, padx=5, pady=10, sticky="nsew")
lName = ctk.CTkLabel(master=fName, text="Nombre:", font=("Helvetica", 14))
lName.pack()

fLastname = ctk.CTkFrame(master=fPatientData, corner_radius=10)
fLastname.grid(row=1, column=2, padx=5, pady=10, sticky="nsew")
lLastname = ctk.CTkLabel(master=fLastname, text="Apellido:", font=("Helvetica", 14))
lLastname.pack()

fDate = ctk.CTkFrame(master=fPatientData, corner_radius=10)
fDate.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
lDate = ctk.CTkLabel(master=fDate, text="Fecha del Examen:", font=("Helvetica", 14))
lDate.pack()

fBirthday = ctk.CTkFrame(master=fPatientData, corner_radius=10)
fBirthday.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
lBirthday = ctk.CTkLabel(master=fBirthday, text="Fecha de nacimiento:", font=("Helvetica", 14))
lBirthday.pack()

fBirthdaySpace = ctk.CTkFrame(master=fPatientData, fg_color=bgRoot)
fBirthdaySpace.grid(row=2, column=1, padx=10, pady=10, sticky="w")
lFormat = ctk.CTkLabel(fBirthdaySpace, text="DD/MM/AAAA")
lFormat.grid(row=0, column= 5, padx=10)

fGender = ctk.CTkFrame(master=fPatientData, corner_radius=10)
fGender.grid(row=2, column=2, padx=5, pady=10, sticky="nsew")
lGender = ctk.CTkLabel(master=fGender, text="Genero:", font=("Helvetica", 14))
lGender.pack()

fDescription = ctk.CTkFrame(master=fPatientData, corner_radius=10)
fDescription.grid(row=3, column=0, padx=5, pady=10, sticky="we")
lDescription = ctk.CTkLabel(master=fDescription, text="Descripción:", font=("Helvetica", 14))
lDescription.pack(fill=Y)

lCount = ctk.CTkLabel(root, text="")
lCount.grid(row=0, column=5, sticky="s")

# Configuración de entradas de datos
entryId = ctk.CTkEntry(master=fPatientData, justify=CENTER, font=("Helvetica", 14), width=200, state="readonly")
entryId.grid(row=0, column=1, padx=10, pady=10, sticky="w")

entryName = ctk.CTkEntry(master=fPatientData, justify=CENTER, font=("Helvetica", 14), width=200, state="readonly")
entryName.grid(row=0, column=3, padx=10, pady=10, sticky="w")


entryLastname = ctk.CTkEntry(master=fPatientData, justify=CENTER, font=("Helvetica", 14), width=200, state="readonly")
entryLastname.grid(row=1, column=3, padx=10, pady=10, sticky="w")

entryDate = ctk.CTkEntry(master=fPatientData, justify=CENTER, font=("Helvetica", 14))
entryDate.insert(0, get_current_date())
entryDate.configure(state="readonly")
entryDate.grid(row=1, column=1, padx=10, pady=10, sticky="w")

textboxDescription = ctk.CTkEntry(fPatientData, font=("Helvetica", 14), state=DISABLED)
textboxDescription.grid(row=3, column=1, rowspan=1, columnspan=3, padx=10, pady=10, sticky="we")

OptionMenuGender = ctk.CTkOptionMenu(master=fPatientData, values=["M", "F", "O"], width=70, state=DISABLED)
OptionMenuGender.set("")
OptionMenuGender.grid(row=2, column=3, padx=10, pady=10, sticky="w")

# Validar solo valores numericos
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

lSeparador1 =ctk.CTkLabel(master=fBirthdaySpace, text="/", font=("Helvetica", 16))
lSeparador1.grid(row=0, column=1, padx=5 )
lSeparador2 =ctk.CTkLabel(master=fBirthdaySpace, text="/", font=("Helvetica", 16))
lSeparador2.grid(row=0, column=3, padx=5 )

# Visor de las imágenes cargadas
fPicture = ctk.CTkFrame(root, fg_color=bgRoot, corner_radius=10, width=400, height=400)
fPicture.grid(row=1, column=5, sticky="nsew", pady=20, padx=10)
fPicture.pack_propagate(FALSE)
lPicture = ctk.CTkLabel(master=fPicture, text="Sin Imagen")
lPicture.pack(expand=TRUE)

# Botones
fButton = ctk.CTkFrame(fPatientData, fg_color=bgRoot)
fButton.grid(row=4, column=1, columnspan=3, padx=10, pady=40, sticky="n")
BLoadImage = ctk.CTkButton(master=fButton, text="Cargar JPG", command=push_cargarbutton)
BSendImage = ctk.CTkButton(master=fButton, text="Convertir a DCM", command=push_convertbutton)
BSend = ctk.CTkButton(master=fButton, text="Enviar Paciente", command=send_button)
BSend.grid(row=0, column=2, padx=20)
BLoadImage.grid(row=0, column=0, padx=20)
BSendImage.grid(row=0, column=1, padx=20)

# Slider para ver imágenes
slider = ctk.CTkSlider(master=root, from_=0, to=100, command=on_slider_change, orientation=VERTICAL, state=DISABLED)
slider.grid(row=1, column=4, rowspan=4, pady=40)


# Fin de la aplicación
root.mainloop()  
