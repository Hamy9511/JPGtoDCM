import tkinter as tk

window = tk.Tk() #Iniciar una a ventana


label1 = tk.Label(
    text = "Hello, Tkinter",
    foreground = "red",
    background ="#000000",
    width = 10,
    height = 10
)
label1.pack()
label2 = tk.Label(
    text = "Hello, Tkinter",
    fg = "black",
    bg ="#34A2FE"
)
label2.pack()

button = tk.Button(
    text = "click me!",
    width = 25,
    height = 5,
    bg = "blue",
    fg = "yellow"
)
button.pack(pady=20) #Padding)

entry = tk.Entry(
    fg="yellow", 
    bg="blue", 
    width=50
)
entry.pack()
window.mainloop()
