import os
import pydicom
from pydicom.dataset import Dataset, FileDataset
from pydicom.uid import generate_uid
from PIL import Image
import datetime

def jpeg_to_dicom(input_jpeg_files, patient_name, patient_id):
    study_instance_uid = generate_uid()
    series_instance_uid = generate_uid()

    # Crear el nombre de la carpeta usando el ID del paciente, nombre del paciente y fecha
    folder_name = f"{patient_id}_{patient_name}_{datetime.date.today()}"

    # Crear la carpeta si no existe
    output_directory = os.path.join(os.getcwd(), folder_name)
    os.makedirs(output_directory, exist_ok=True)

    for i, input_jpeg_file in enumerate(input_jpeg_files):
        # Leer la imagen JPEG
        image = Image.open(input_jpeg_file)
        image = image.convert("RGB")  # Asegurarse de que la imagen esté en formato RGB

        # Crear un objeto Dataset DICOM vacío
        file_meta = pydicom.dataset.FileMetaDataset()
        file_meta.MediaStorageSOPClassUID = pydicom.uid.SecondaryCaptureImageStorage
        file_meta.MediaStorageSOPInstanceUID = generate_uid()
        file_meta.ImplementationClassUID = generate_uid()

        ds = FileDataset(None, {}, file_meta=file_meta, preamble=b"\0" * 128)

        # Establecer los metadatos necesarios
        ds.PatientName = patient_name
        ds.PatientID = patient_id
        ds.StudyInstanceUID = study_instance_uid
        ds.SeriesInstanceUID = series_instance_uid
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

        # Convertir la imagen JPEG a píxeles y almacenarla como píxeles RGB
        pixel_array = image.tobytes()
        ds.PixelData = pixel_array

        # Añadir información adicional requerida
        ds.Modality = 'OT'  # Other
        ds.ContentDate = str(datetime.date.today()).replace('-', '')
        ds.ContentTime = str(datetime.datetime.now().time()).replace(':', '').split('.')[0]

        # Estudio y Serie
        ds.StudyID = "1"
        ds.SeriesNumber = "1"
        ds.InstanceNumber = str(i + 1)

        # Guardar el archivo DICOM
        ds.is_little_endian = True
        ds.is_implicit_VR = True

        output_dicom_file = os.path.join(output_directory, f"{patient_id}_{patient_name}_{datetime.date.today()}_{i + 1}.dcm")
        ds.save_as(output_dicom_file, write_like_original=False)
        print(f"Archivo DICOM guardado como {output_dicom_file}")

# Ejemplo de uso
input_jpeg_files = ["input1.jpg", "input2.jpg", "input3.jpg"]
jpeg_to_dicom(input_jpeg_files, patient_name="PRUEBA", patient_id="123456789634634355346")
