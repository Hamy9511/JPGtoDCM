import customtkinter as ctk
from tkcalendar import Calendar

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Ejemplo de Calendario con customtkinter")
        self.geometry("400x400")

        # Crear el calendario usando tkcalendar
        self.calendar = Calendar(self, selectmode='day', year=2023, month=7, day=1)
        self.calendar.pack(pady=20)

        # Botón para mostrar la fecha seleccionada
        self.show_date_button = ctk.CTkButton(self, text="Mostrar Fecha Seleccionada", command=self.show_date)
        self.show_date_button.pack(pady=10)

    def show_date(self):
        selected_date = self.calendar.get_date()
        print(f"Fecha seleccionada: {selected_date}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
