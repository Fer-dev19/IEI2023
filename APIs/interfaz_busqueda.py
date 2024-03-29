import tkinter as tk
from tkinter import ttk, messagebox
import requests
import tkintermapview
from tkinterweb import HtmlFrame
import interfaz_carga

#Funcion que obtiene los centros buscados
def filtrar():
    #Funcion que indica en los campos de busqueda cual es el centro sobre el que se ha hecho click
    def mostrarDatos(marker):
        localidadInput.delete(0, tk.END)
        provinciaInput.delete(0, tk.END)
        codPostalInput.delete(0, tk.END)
        for centro in centros:
            if centro.get('nombre') == marker.data:
                localidadInput.insert(tk.END, centro.get('localidad'))
                codPostalInput.insert(tk.END, centro.get('codigo_postal'))
                provinciaInput.insert(tk.END, centro.get('provincia'))
                for tipo in tipoOptions:
                    if centro.get('tipo') == tipo:
                        variableControlTipo.set(tipo)
                        break

                # Crear una ventana emergente
                popup = tk.Toplevel()
                popup.title("Información del Centro")

                # Configurar la posición de la ventana emergente
                popup.geometry("+{}+{}".format(ventana.winfo_x() + 700, ventana.winfo_y() + 150))

                # Mostrar más información en la ventana emergente
                info = f"Nombre: {centro.get('nombre')}\n"
                info += f"Tipo: {centro.get('tipo')}\n"
                info += f"Dirección: {centro.get('direccion')}\n"
                info += f"Código Postal: {centro.get('codigo_postal')}\n"
                info += f"Teléfono: {centro.get('telefono')}\n"
                info += f"Descripción: {centro.get('descripcion')}\n"
                info += f"Localidad: {centro.get('localidad')}\n"
                info += f"Provincia: {centro.get('provincia')}\n"
                label = tk.Label(popup, text=info, wraplength=250, justify=tk.LEFT)
                label.pack()

    #Peticion a base de datos para obtener los centros
    url = 'http://127.0.0.1:5004/buscar'
    # Parámetros a pasar para filtrar
    params = {'localidad': localidadInput.get(), 'codPostal': codPostalInput.get(), 'provincia': provinciaInput.get(),
              'tipo': variableControlTipo.get()}
    response = requests.get(url, params=params)
    #Procesamiento de la respuesta
    #Por cada centro se obtienen sus datos, si estos constan de latitud y longitud se añadira un marcador en el mapa
    #Finalmente cada registro de centro se añade a la tabla de resultado donde se mostrara.
    if response.status_code == 200:
        map_widget.delete_all_marker()
        resultTable.delete(*resultTable.get_children())
        centros = response.json()
        for centro in centros:
            nombre = centro.get('nombre', 'Nombre no disponible')
            codPostal = centro.get('codigo_postal', 'Codigo postal no disponible')
            localidad = centro.get('localidad', 'Localidad no disponible')
            provincia = centro.get('provincia', 'Provincia no disponible')
            direccion = centro.get('direccion', 'Dirección no disponible')
            tipo = centro.get('tipo', 'Tipo no disponible')
            latitud = centro.get('latitud', 'Latitud no disponible')
            longitud = centro.get('longitud', 'Longitud no disponible')
            telefono = centro.get('telefono', 'Teléfono no disponible')
            descripcion = centro.get('descripcion', 'Descripción no disponible')

            if latitud is not None and longitud is not None:
                map_widget.set_marker(latitud, longitud, nombre, data=nombre, command=mostrarDatos)

            info_localidad = f"Nombre: {nombre}, Localidad: {localidad}, Provincia: {provincia}, Dirección: {direccion}\n"
            resultTable.insert('', tk.END, values=(
                nombre, tipo, direccion, codPostal, telefono, descripcion, localidad, provincia))
    elif response.status_code == 404:
        print('Localidad no encontrada')
        map_widget.delete_all_marker()
        resultTable.delete(*resultTable.get_children())
        resultTable.insert('', tk.END, values=('no hay resultados'))
    else:
        print(f'Error en la solicitud: {response.status_code}')


# Funcion que abre la interfaz de carga de datos
def cargar():
    interfaz_carga.abrir_interfaz_carga(ventana)


# Crear ventana principal de la interfaz
ventana = tk.Tk()
ventana.title("Buscador de centros educativos")
ventana.geometry("1280x720")
ventana.resizable(False, False)

# Etiqueta titulo
etiqueta = tk.Label(ventana, text="Buscador de centros educativos", font=("Arial", 26))
etiqueta.place(x=400, y=30)

frame_inputs = tk.Frame(ventana)
frame_inputs.place(x=300, y=120)

# Crear las distintas etiquetas de los campos de busqueda
labels = ["Localidad:", "Cod. Postal:", "Provincia:", "Tipo:"]
entries = [None, None, None]
for i, label in enumerate(labels):
    tk.Label(frame_inputs, text=label, font=("Arial", 16)).grid(row=i, column=0, sticky='e')
    if i < 3:
        entries[i] = tk.Entry(frame_inputs)
        entries[i].grid(row=i, column=1)

# Crear los elementos de entrada de datos para busqueda
localidadInput, codPostalInput, provinciaInput = entries

# Crear el input menu desplegable de la interfaz
tipoOptions = ["Público", "Privado", "Concertado", "Otros", "Todos"]
variableControlTipo = tk.StringVar(ventana)
variableControlTipo.set(tipoOptions[0])
tipoInput = tk.OptionMenu(frame_inputs, variableControlTipo, *tipoOptions)
tipoInput.grid(row=3, column=1, sticky='w')

# Crear los botones de la interfaz
cancelar = tk.Button(ventana, text="Cancelar", command=ventana.destroy)
cancelar.place(x=380, y=260)
aceptar = tk.Button(ventana, text="Aceptar", command=filtrar)
aceptar.place(x=480, y=260)
cargar = tk.Button(ventana, text="Cargar", command=cargar)
cargar.place(x=380, y=300)

# Crear y configurar la tabla Treeview con columnas adicionales
columns = ("nombre", "tipo", "direccion", "codigo_postal", "telefono", "descripcion", "localidad", "provincia")
resultTable = ttk.Treeview(ventana, columns=columns, show='headings', xscrollcommand=True, yscrollcommand=True)

# Configurar las barras de desplazamiento para la tabla
scrollbar_vertical = ttk.Scrollbar(ventana, orient="vertical", command=resultTable.yview)
scrollbar_horizontal = ttk.Scrollbar(ventana, orient="horizontal", command=resultTable.xview)
resultTable.configure(yscrollcommand=scrollbar_vertical.set, xscrollcommand=scrollbar_horizontal.set)

# Posicionar la tabla y las barras de desplazamiento en la ventana
resultTable.place(x=200, y=500, height=200, width=800)
scrollbar_vertical.place(x=1000, y=500, height=200)
scrollbar_horizontal.place(x=200, y=700, width=800)

# Definir encabezados de la tabla
for col in columns:
    resultTable.heading(col, text=col.capitalize())

# Crear el mapa de la interfaz
map_widget = tkintermapview.TkinterMapView(ventana, width=400, height=400, corner_radius=0)
map_widget.place(x=800, y=275, anchor=tk.CENTER)
map_widget.set_position(40.417278703578596, -3.701168707505883)
map_widget.set_zoom(6)

# Ejecutar la ventana
ventana.mainloop()
