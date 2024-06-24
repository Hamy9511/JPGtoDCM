import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, Image

ventana = tk.Tk()
ventana.title("Envio de paciente DICOM ")
ventana.geometry("600x1000")

etiqueta = tk.Label(ventana, text="ID DE PACIENTE")
etiqueta.pack()

def seleccionar_imagen():
    ruta_imagen = filedialog.askopenfilename(title="Seleccionar Imagen", filetypes=[("Archivos de imagen", "*.png *.jpg *.jpeg")])
    if ruta_imagen:
        imagen_pil = Image.open(ruta_imagen)
        imagen_pil = imagen_pil.resize((200, 200), Image.ANTIALIAS) 
        imagen = ImageTk.PhotoImage(imagen_pil)
        etiqueta_imagen.configure(image=imagen)
        etiqueta_imagen.image = imagen

def boton_click():
    texto = entrada.get()
    messagebox.showinfo("Confirmación", f"Has Enviado: {texto}")

entrada = tk.Entry(ventana, width=40)
entrada.pack()

boton_seleccionar = tk.Button(ventana, text="Seleccionar Imagen", command=seleccionar_imagen)
boton_seleccionar.pack()

boton_enviar = tk.Button(ventana, text= "Enviar", command=boton_click)
boton_enviar.pack()

etiqueta_imagen = tk.Label(ventana, width=200, height=200)
etiqueta_imagen.pack()


ventana.mainloop()