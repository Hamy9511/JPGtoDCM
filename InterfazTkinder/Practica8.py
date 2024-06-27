import tkinter as tk

window = tk.Tk()
def handle_click(event):
    print("The button was clicked!")

button = tk.Button(text="Click me!")

button.bind("<Button-1>", handle_click) #"<Button-1>" Click Izquierdo,   <Button-2>" Click Central, <Button-3>" Click derecho,
button.pack()
window.mainloop()

