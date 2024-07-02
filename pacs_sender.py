import os
import sys
import uuid
import tkinter as tk
from tkinter import messagebox
from pydicom import dcmread
from pydicom.uid import UID
from pynetdicom import AE, StoragePresentationContexts

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

def main():
    if len(sys.argv) < 2:
        print("Uso: pacs_sender.py <directorio>")
        return

    # Directorio con las imágenes DICOM
    folder_path = sys.argv[1]
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

if __name__ == '__main__':
    main()
