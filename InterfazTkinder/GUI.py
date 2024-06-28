import tkinter as tk #Libreria para interfaz

#CONFIGURACION DE VENTANA
window = tk.Tk() #Crear ventana con nombre Tkinter
window.config() #Configuracion de estilos de la ventana
window.title("JPGtoDICOM Sender") #Titulo de la ventana
window.geometry("400x700") #Dimensiones de la ventana
window.resizable(0,0) #Configurando si o no se puede redimencionar la ventana 0 = false, 1 = True (width, height)

#CONFIGURACION DE GRID
window.columnconfigure(0,weight=1) #Configuracionde columnas tipo grid (index,weight)
window.columnconfigure(1,weight=3)
#window.rowconfigure() #Configuración de filas tipo grid (index,weight)

#CONFIGURACION DE LABELS DE DATOS DEL PACIENTE

#Titulo
fInput = tk.Frame(window, bg="gray", padx=5, pady=5, borderwidth=5, relief="sunken") #Creación de un cajon
fInput.grid(row=0, column=0, rowspan=1, columnspan=2, sticky=tk.NSEW, padx=20, pady=20,) #Asignar y configurar celda del grid
lInput = tk.Label(master=fInput, text="INGRESAR DATOS DEL PACIENTE", font=("arial", 14, "bold italic"), bg="gray") #Label asignado al frame
#lInput.config(font=("arial", 14, "bold italic")) <-------------- Otra forma de agregar cambios al frame, label, etc.
lInput.pack() #Ejecutando el label

#ID
fId = tk.Frame(master=window)
fId.grid(row=1, column=0, padx=10, pady=10)
lId = tk.Label(master=fId, text="ID del paciente:", font=("arial", 10))
lId.pack()

#Nombre
fName = tk.Frame(master=window)
fName.grid(row=2, column=0, padx=10, pady=10)
lName = tk.Label(master=fName, text="Nombre:", font=("arial", 10))
lName.pack()

#Apellido
fLastname = tk.Frame(master=window)
fLastname.grid(row=3, column=0, padx=10, pady=10)
lLastname = tk.Label(master=fLastname, text="Apellido:", font=("arial", 10))
lLastname.pack()

#Fecha
fDate = tk.Frame(master=window)
fDate.grid(row=4, column=0, padx=10, pady=10)
lDate = tk.Label(master=fDate, text="Fecha del Examen:", font=("arial", 10))
lDate.pack()
<<<<<<< HEAD

#CONFIGURACION DE TEXTBOX

fEntryId = tk.Frame(window)
fEntryId.grid(row=1, column=1, padx=10, pady=10)
entryId = tk.Entry(master=fEntryId)
entryId.pack()

fEntryName = tk.Frame(window)
fEntryName.grid(row=2, column=1, padx=10, pady=10)
entryName = tk.Entry(master=fEntryName)
entryName.pack()

fEntryLastname = tk.Frame(window)
fEntryLastname.grid(row=3, column=1, padx=10, pady=10)
entryLastname = tk.Entry(master=fEntryLastname)
entryLastname.pack()

fEntryDate = tk.Frame(window)
fEntryDate.grid(row=4, column=1, padx=10, pady=10)
entryDate = tk.Entry(master=fEntryDate)
entryDate.pack()


=======

>>>>>>> 61d0721dfcf8fe52633979696c888e58824a4ce7
window.mainloop() #Fin de app