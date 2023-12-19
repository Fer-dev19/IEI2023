import tkinter as tk
from interfaz_busqueda import BuscadorCentrosEducativos
from interfaz_carga import CargaDatos

class AplicacionPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplicación Principal")
        self.geometry("1200x675")

        # Inicializar la primera interfaz
        self.mostrar_buscador_centros()

    def mostrar_buscador_centros(self):
        # Mostrar la interfaz del buscador de centros educativos
        frame = BuscadorCentrosEducativos(self, self.mostrar_carga_datos)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def mostrar_carga_datos(self):
        # Mostrar la interfaz de carga de datos
        frame = CargaDatos(self, self.mostrar_buscador_centros)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

if __name__ == "__main__":
    app = AplicacionPrincipal()
    app.mainloop()
