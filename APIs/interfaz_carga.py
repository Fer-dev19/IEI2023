import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading

# Suponiendo que 'cargar_datos' es la función de tu API que deseas llamar
from API_Carga import cargar_datos

def abrir_interfaz_carga(parent_root):

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

    ventana_carga = tk.Toplevel(parent_root)
    ventana_carga.title("Carga del almacén de datos")
    ventana_carga.geometry("800x600")  # Ancho x Alto

    # Frame para contener todos los elementos y centrarlos
    frame = tk.Frame(ventana_carga)
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
    boton_cancelar = tk.Button(frame, text="Cancelar", command=ventana_carga.quit)
    boton_cancelar.pack(side=tk.RIGHT, padx=10, pady=20)

    # Área de texto con barras de desplazamiento para mostrar los resultados
    resultados_carga = scrolledtext.ScrolledText(frame, height=10, width=50)
    resultados_carga.pack(pady=10)

    # Ejecutar la GUI
    ventana_carga.mainloop()
