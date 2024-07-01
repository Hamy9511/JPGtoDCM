from pynetdicom import AE, StoragePresentationContexts
from pydicom import dcmread

# Dirección y puerto del servidor PACS (Orthanc en este caso)
PACS_IP = '192.168.2.100'  # IP de tu servidor Orthanc
PACS_PORT = 4242  # Puerto de tu servidor Orthanc
PACS_AET = b'Pato_Pacs'  # AET del servidor Orthanc

# Puerto local en el que escuchará el AE
LOCAL_PORT = 4242  # Puerto local, ajusta según tu configuración

def enviar_imagenes_dicom(dicom_files):
    # Cargar las imágenes DICOM
    imagenes_dicom = [dcmread(file) for file in dicom_files]

    # Configurar el AE (Application Entity)
    ae = AE(ae_title=b'DCMSEND', port=LOCAL_PORT)  # Nombre del AE local y puerto local
    
    # Agregar contextos de presentación para almacenamiento
    for context in StoragePresentationContexts:
        ae.add_requested_context(context.abstract_syntax, transfer_syntax=context.transfer_syntax[0])

    # Método para manejar las solicitudes C-STORE
    def on_c_store(ds, context, info):
        # Aquí puedes agregar tu lógica para manejar las imágenes recibidas
        # Por ejemplo, guardar las imágenes en un directorio local o procesarlas de alguna manera
        return 0x0000  # Devuelve un código de estado de éxito

    # Asignar la función on_c_store al evento 'evt.on_c_store'
    ae.on_c_store = on_c_store

    # Establecer la conexión con el servidor PACS
    assoc = ae.associate(PACS_IP, PACS_PORT, ae_title=PACS_AET)

    if assoc.is_established:
        # Enviar cada imagen DICOM
        for imagen in imagenes_dicom:
            status = assoc.send_c_store(imagen)

            # Verificar el estado del envío
            if status:
                print(f'Imagen {imagen.SOPInstanceUID} enviada correctamente')
            else:
                print(f'Error al enviar la imagen {imagen.SOPInstanceUID}')

        # Finalizar la asociación
        assoc.release()
    else:
        print('No se pudo establecer la conexión con el servidor PACS')
