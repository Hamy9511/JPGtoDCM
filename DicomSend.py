import os
from pydicom import dcmread
from pynetdicom import AE, StoragePresentationContexts

# Dirección y puerto del servidor PACS
PACS_IP = '186.151.231.22'
PACS_PORT = 104

# Ruta de las imágenes DICOM
DICOM_DIR = '../ImageConverter/123456789634634355346_PRUEBA_2024-06-09'

def enviar_imagenes_dicom():
    # Cargar las imágenes DICOM
    imagenes_dicom = [dcmread(os.path.join(DICOM_DIR, imagen)) for imagen in os.listdir(DICOM_DIR)]

    # Configurar el AE (Application Entity)
    ae = AE()
    ae.ae_title = b'MI_AE'  # Nombre del AE local
    ae.port = 11113  # Puerto en el que escuchará el AE

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
    assoc = ae.associate(PACS_IP, PACS_PORT)

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

if __name__ == '__main__':
    enviar_imagenes_dicom()
