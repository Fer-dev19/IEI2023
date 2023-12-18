# import tkinter as tk
# from tkinter import messagebox
# import threading

# # Suponiendo que 'cargar_datos' es la función de tu API que deseas llamar
# from API_Carga import cargar_datos

# def iniciar_carga(comunidades):
#     # Ejecuta la carga de datos en un hilo separado para no bloquear la GUI
#     def carga():
#         try:
#             cargar_datos(comunidades)
#             messagebox.showinfo("Éxito", "Los datos han sido cargados con éxito.")
#         except Exception as e:
#             messagebox.showerror("Error", f"Ha ocurrido un error durante la carga: {e}")

#     thread = threading.Thread(target=carga, daemon=True)
#     thread.start()

# # Función llamada cuando se presiona el botón 'Cargar'
# def on_cargar():
#     # Obtiene las comunidades seleccionadas
#     seleccionadas = [comunidad for comunidad, var in checkboxes.items() if var.get()]
#     if not seleccionadas:
#         messagebox.showwarning("Advertencia", "Por favor, seleccione al menos una comunidad para cargar.")
#         return
#     iniciar_carga(seleccionadas)

# root = tk.Tk()
# root.title("Carga del almacén de datos")
# root.geometry("800x600")  # Ancho x Alto

# # Diccionario para almacenar las variables de las casillas de verificación
# checkboxes = {}

# # Casilla de verificación 'Seleccionar todas'
# var_todas = tk.BooleanVar()
# cb_todas = tk.Checkbutton(root, text="Seleccionar todas", variable=var_todas,
#                           command=lambda: [var.set(var_todas.get()) for var in checkboxes.values()])
# cb_todas.grid(row=0, columnspan=2, sticky='w')

# # Casillas de verificación para cada comunidad
# comunidades = ["Murcia", "Valencia", "Cataluña"]
# for i, comunidad in enumerate(comunidades, start=1):
#     var = tk.BooleanVar()
#     cb = tk.Checkbutton(root, text=comunidad, variable=var)
#     cb.grid(row=i, column=0, sticky='w')
#     checkboxes[comunidad] = var

# # Botón 'Cargar'
# boton_cargar = tk.Button(root, text="Cargar", command=on_cargar)
# boton_cargar.grid(row=i+1, column=0)

# # Botón 'Cancelar'
# boton_cancelar = tk.Button(root, text="Cancelar", command=root.quit)
# boton_cancelar.grid(row=i+1, column=1)

# # Ejecutar la GUI
# root.mainloop()

import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading

# Suponiendo que 'cargar_datos' es la función de tu API que deseas llamar
from API_Carga import cargar_datos

def iniciar_carga(comunidades, resultados_carga):
    # Ejecuta la carga de datos en un hilo separado para no bloquear la GUI
    def carga():
        try:
            cargar_datos(comunidades)
            resultados_carga.insert(tk.END, "Los datos han sido cargados con éxito.\n")
        except Exception as e:
            resultados_carga.insert(tk.END, f"Ha ocurrido un error durante la carga: {e}\n")

    thread = threading.Thread(target=carga, daemon=True)
    thread.start()

# Función llamada cuando se presiona el botón 'Cargar'
def on_cargar(resultados_carga):
    # Obtiene las comunidades seleccionadas
    seleccionadas = [comunidad for comunidad, var in checkboxes.items() if var.get()]
    if not seleccionadas:
        messagebox.showwarning("Advertencia", "Por favor, seleccione al menos una comunidad para cargar.")
        return
    resultados_carga.delete(1.0, tk.END)  # Limpiar el área de texto
    iniciar_carga(seleccionadas, resultados_carga)

root = tk.Tk()
root.title("Carga del almacén de datos")
root.geometry("800x600")  # Ancho x Alto

# Frame para contener todos los elementos y centrarlos
frame = tk.Frame(root)
frame.pack(expand=True)

# Diccionario para almacenar las variables de las casillas de verificación
checkboxes = {}

# Casilla de verificación 'Seleccionar todas'
var_todas = tk.BooleanVar()
cb_todas = tk.Checkbutton(frame, text="Seleccionar todas", variable=var_todas,
                          command=lambda: [var.set(var_todas.get()) for var in checkboxes.values()])
cb_todas.pack(anchor='center')

# Casillas de verificación para cada comunidad
comunidades = ["Murcia", "Valencia", "Cataluña"]
for comunidad in comunidades:
    var = tk.BooleanVar()
    cb = tk.Checkbutton(frame, text=comunidad, variable=var)
    cb.pack(anchor='center')
    checkboxes[comunidad] = var

# Botón 'Cargar'
boton_cargar = tk.Button(frame, text="Cargar", command=lambda: on_cargar(resultados_carga))
boton_cargar.pack(side=tk.LEFT, padx=10, pady=20)

# Botón 'Cancelar'
boton_cancelar = tk.Button(frame, text="Cancelar", command=root.quit)
boton_cancelar.pack(side=tk.RIGHT, padx=10, pady=20)

# Área de texto con barras de desplazamiento para mostrar los resultados
resultados_carga = scrolledtext.ScrolledText(frame, height=10, width=50)
resultados_carga.pack(pady=10)

# Ejecutar la GUI
root.mainloop()
