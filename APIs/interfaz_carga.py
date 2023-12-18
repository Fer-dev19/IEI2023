import tkinter as tk
from tkinter import messagebox
import threading

# Suponiendo que 'cargar_datos' es la función de tu API que deseas llamar
from API_Carga import cargar_datos

def iniciar_carga(comunidades):
    # Ejecuta la carga de datos en un hilo separado para no bloquear la GUI
    def carga():
        try:
            cargar_datos(comunidades)
            messagebox.showinfo("Éxito", "Los datos han sido cargados con éxito.")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error durante la carga: {e}")

    thread = threading.Thread(target=carga, daemon=True)
    thread.start()

# Función llamada cuando se presiona el botón 'Cargar'
def on_cargar():
    # Obtiene las comunidades seleccionadas
    seleccionadas = [comunidad for comunidad, var in checkboxes.items() if var.get()]
    if not seleccionadas:
        messagebox.showwarning("Advertencia", "Por favor, seleccione al menos una comunidad para cargar.")
        return
    iniciar_carga(seleccionadas)

root = tk.Tk()
root.title("Carga del almacén de datos")

# Diccionario para almacenar las variables de las casillas de verificación
checkboxes = {}

# Casilla de verificación 'Seleccionar todas'
var_todas = tk.BooleanVar()
cb_todas = tk.Checkbutton(root, text="Seleccionar todas", variable=var_todas,
                          command=lambda: [var.set(var_todas.get()) for var in checkboxes.values()])
cb_todas.grid(row=0, columnspan=2, sticky='w')

# Casillas de verificación para cada comunidad
comunidades = ["Murcia", "Comunitat Valenciana", "Catalunya"]
for i, comunidad in enumerate(comunidades, start=1):
    var = tk.BooleanVar()
    cb = tk.Checkbutton(root, text=comunidad, variable=var)
    cb.grid(row=i, column=0, sticky='w')
    checkboxes[comunidad] = var

# Botón 'Cargar'
boton_cargar = tk.Button(root, text="Cargar", command=on_cargar)
boton_cargar.grid(row=i+1, column=0)

# Botón 'Cancelar'
boton_cancelar = tk.Button(root, text="Cancelar", command=root.quit)
boton_cancelar.grid(row=i+1, column=1)

# Ejecutar la GUI
root.mainloop()
