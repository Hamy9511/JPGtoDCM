import customtkinter as ctk

# Función para manejar la selección del OptionMenu
def seleccionar_opcion(valor):
    print(f"Opción seleccionada: {valor}")

# Crear la ventana principal
root = ctk.CTk()
root.geometry("300x200")

# Lista de opciones para el OptionMenu
opciones = ["Opción 1", "Opción 2", "Opción 3", "Opción 4", "Opción 5",
            "Opción 6", "Opción 7", "Opción 8", "Opción 9", "Opción 10"]

# Crear el OptionMenu
opcion_menu = ctk.CTkOptionMenu(root, value=opciones, command=seleccionar_opcion)
opcion_menu.pack(pady=20)

# Configurar la altura máxima del menú desplegable (opcional)
opcion_menu.configure(menu_height=4)

root.mainloop()
