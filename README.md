# CONVERTIDOR DE JPG A DICOM

Generador imgenes .DCM con compatibilidad para sistemas PACS (Picture Archiving and Communication System) a partir
de imagenes JPG exportadas por sistemas, modalidades o equipos de captura de imagenes.
## Tabla de Contenidos

- [Descripción](#descripción)
- [Características](#características)
- [Instalación](#instalación)
- [Uso](#uso)
- [Contacto](#contacto)

## Descripción

El programa permite seleccionar imágenes en .JPG de las cuales pueden ser visibles en la interfaz una por una por medio de un Slider
(Solamente para referencia de las imágenes que se van a enviar), luego el programa exige al usuario que ponga los datos del paciente
que serán vinculados a la serie de imágenes seleccionadas (Mínimo se deben de colocar ID; Nombre y Apellidos), la fecha de adquisición
de adquisición del estudio es tomada del momento de la selección de las imágenes .JPG y la información como "Descripción, Género y Fecha de nacimiento"
son opcionales.

Al tener todos los datos mínimos del paciente llenos, se convierten a .DCM en una carpeta llamada dicom_files ubicado en el directorio del programa
y se crea una carpeta con todas la serie de imágenes con el nombre de ID y nombre del paciente.

Por último se ha añadido una función de envío a PACS, el cual abre el explorador de archivos para seleccionar la carpeta de imágenes  .DCM
para luego realizar un envío de las imágenes con toda la info anidada al PACS de su preferencia.

## Características

- Convertidor de .JPG a .DCM
- Capacidad de anidar o vincular información básica del paciente
- Envío a PACS

## Instalación

En la carpeta dist/main se encuentra el aplicativo. Al iniciar por primera vez genera dos carpetas JPG_images y dicom_files.

## Uso
Uso no clinico, actualmente solo se utiliza para imagenes de referencia.

## Contacto

https://github.com/Hamy9511/
https://www.linkedin.com/in/hamiltonduran

```bash
# Clona el repositorio
git clone https://github.com/Hamy9511/JPGtoDCM.git
