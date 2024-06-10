import os
import pydicom
from pydicom.dataset import Dataset, FileDataset
from pydicom.uid import generate_uid
from PIL import Image
import datetime

def jpeg_to_dicom(input_jpeg_file, output_dicom_file):
    # Leer la imagen JPEG
    image = Image.open(input_jpeg_file)
    image = image.convert("RGB")  # Asegurarse de que la imagen esté en formato RGB

    # Crear un objeto Dataset DICOM vacío
    file_meta = pydicom.dataset.FileMetaDataset()
    file_meta.MediaStorageSOPClassUID = pydicom.uid.SecondaryCaptureImageStorage
    file_meta.MediaStorageSOPInstanceUID = generate_uid()
    file_meta.ImplementationClassUID = generate_uid()
    
    ds = FileDataset(output_dicom_file, {}, file_meta=file_meta, preamble=b"\0" * 128)

    # Establecer los metadatos necesarios
    ds.PatientName = "PRUEBA DE JPG A DICOM"
    ds.PatientID = "1234567890"
    ds.StudyInstanceUID = generate_uid()
    ds.SeriesInstanceUID = generate_uid()
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
    ds.StudyID = "PRUEBA1"
    ds.SeriesNumber = "1"
    ds.InstanceNumber = "1"

    # Guardar el archivo DICOM
    ds.is_little_endian = True
    ds.is_implicit_VR = True

    ds.save_as(output_dicom_file, write_like_original=False)
    print(f"Archivo DICOM guardado como {output_dicom_file}")

# Ejemplo de uso
input_jpeg_file = "input.jpg"
output_dicom_file = "output.dcm"
jpeg_to_dicom(input_jpeg_file, output_dicom_file)
