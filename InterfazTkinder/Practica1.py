import tkinter as tk

window = tk.Tk()

label = tk.Label(text = "Name")
entry = tk.Entry()
label.pack()
entry.pack()

entry.insert(0, "Real Hasta La Muerte") #insertar un texto en la entrada de text
entry.delete(0, 2) #Borrar de la posicion 0 a la 2 nota: tk.END borra todo
name = entry.get() #Adquirir lo que esta dentro de la entrada de text
name

text_box = tk.Text()
text_box.pack()

text_box.get("1.0, 1.5") #De la linea 1, conseguir las letras de la posicion 0 a la 5
text_box.delete("1.0, 1.5")
text_box.insert("2.0", "\nWorld") #insertar con salto de linea a la segunda linea posicion 0
#window.destroy() Cerrar ventana 
window.mainloop()