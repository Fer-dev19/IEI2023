import tkinter as tk
import requests
import interfaz_carga


def buscar():

    def mostrarDatos(marker):
        localidadInput.delete(0, tk.END)
        provinciaInput.delete(0, tk.END)
        codPostalInput.delete(0, tk.END)
        print(marker.data)
        for centro in centros:
            if centro.get('nombre') == marker.data:
                localidadInput.insert(tk.END,centro.get('localidad'))
                codPostalInput.insert(tk.END, centro.get('codigo_postal'))
                provinciaInput.insert(tk.END, centro.get('provincia'))
                for tipo in tipoOptions:
                    if centro.get('tipo') == tipo:
                        variableControlTipo.set(tipo)
                        break
                break

    url = 'http://127.0.0.1:5004/getCentros'
    #Peticioon para obtener todos los centros
    params = {'provincia': "Barcelona"}
    response = requests.get(url)
    if response.status_code == 200:
        centros = response.json()

        for centro in centros:
            # Accediendo a los atributos específicos de cada localidad
            nombre = centro.get('nombre', 'Nombre no disponible')
            codPostal = centro.get('codigo_postal', 'Codigo postal no disponible')
            localidad_nombre = centro.get('localidad', 'Localidad no disponible')
            provincia = centro.get('provincia', 'Provincia no disponible')
            direccion = centro.get('direccion', 'Dirección no disponible')
            tipo = centro.get('tipo', 'Tipo no disponible')
            latitud = centro.get('latitud', 'Latitud no disponible')
            longitud = centro.get('longitud', 'Longitud no disponible')

            #Estableciendo marcadores
            if latitud is not None and longitud is not None:
                map_widget.set_marker(latitud,longitud,nombre,data=nombre,command=mostrarDatos)

            # Formateando la cadena para mostrar la información deseada
            info_localidad = f"Nombre: {nombre}, Localidad: {localidad_nombre}, Provincia: {provincia}, Dirección: {direccion}\n"

            # Insertando la cadena en resultText
            resultText.insert(tk.END, info_localidad)
    elif response.status_code == 404:
        resultText.insert(tk.END,"No hay resultados")
    else:
        resultText.insert(tk.END, "Error")


def cargar():
    interfaz_carga.abrir_interfaz_carga(ventana)

import tkintermapview
from tkinterweb import HtmlFrame  # Para mostrar HTML en Tkinter

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Buscador de centros educativos")

# Establecer el tamaño inicial de la ventana (ancho x alto)
ventana.geometry("1200x675")
ventana.resizable(False, False)

# Establecer etiqueta principal
etiqueta = tk.Label(ventana, text="Buscador de centros educativos", font=("Arial", 26))
etiqueta.place(x=400, y=60)

# Crear una variable de control para el menú
variableControlTipo = tk.StringVar(ventana)
variableControlTipo.set("Público")  # Opción predeterminada

# Establecer pares etiqueta e inputText
localidad = tk.Label(ventana, text="Localidad:", font=("Arial", 16))
localidad.place(x=300, y=120)
localidadInput = tk.Entry(ventana)
localidadInput.place(x=400, y=120)
codPostal = tk.Label(ventana, text="Cod. Postal:", font=("Arial", 16))
codPostal.place(x=285, y=150)
codPostalInput = tk.Entry(ventana)
codPostalInput.place(x=400, y=150)
provincia = tk.Label(ventana, text="Provincia:", font=("Arial", 16))
provincia.place(x=300, y=180)
provinciaInput = tk.Entry(ventana)
provinciaInput.place(x=400, y=180)
tipo = tk.Label(ventana, text="Tipo:", font=("Arial", 16))
tipo.place(x=335, y=210)
tipoOptions = ["Público", "Privado", "Concertado", "Otros"]
tipoInput = tk.OptionMenu(ventana, variableControlTipo,tipoOptions[0], *tipoOptions)
tipoInput.place(x=400, y=210)
resultLabel = tk.Label(ventana, text="Resultados de la Busqueda:", font=("Arial", 16))
resultLabel.place(x=300, y=400)

# Establecer botones
cancelar = tk.Button(ventana, text="Cancelar")
cancelar.place(x=380, y=260)
aceptar = tk.Button(ventana, text="Aceptar", command=buscar)
aceptar.place(x=480, y=260)
cargar = tk.Button(ventana, text="Cargar", command=cargar)
cargar.place(x=380, y=300)

# Establecer texto resultado
resultText = tk.Text(ventana, height=15, width=110)
resultText.place(x=200, y=450)

# Configurar columnas
ventana.columnconfigure(0, weight=1)
ventana.columnconfigure(1, weight=2)

# create map widget
map_widget = tkintermapview.TkinterMapView(ventana, width=325, height=325, corner_radius=0)
map_widget.place(x=800, y=275, anchor=tk.CENTER)

# set current widget position and zoom
map_widget.set_position(40.417278703578596, -3.701168707505883)  # Madrid, Spain
map_widget.set_zoom(10)

# Iniciar el bucle de eventos
ventana.mainloop()
