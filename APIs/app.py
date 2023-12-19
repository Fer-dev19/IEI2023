import tkinter as tk
from interfaz_busqueda import abrir_interfaz_busqueda
from interfaz_carga import abrir_interfaz_carga

def main():
    root = tk.Tk()
    root.title("Aplicación Principal")
    root.geometry("300x200")

    # Botón para abrir la interfaz de búsqueda
    boton_busqueda = tk.Button(root, text="Abrir Interfaz de Búsqueda", command=abrir_interfaz_busqueda)
    boton_busqueda.pack(pady=10)

    # Botón para abrir la interfaz de carga
    boton_carga = tk.Button(root, text="Abrir Interfaz de Carga", command=lambda: abrir_interfaz_carga(root))
    boton_carga.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
