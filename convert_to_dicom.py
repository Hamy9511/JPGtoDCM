# Converitr JPG a DCM
import os
from datetime import datetime
import pydicom
from pydicom.dataset import FileDataset
from pydicom.uid import generate_uid

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