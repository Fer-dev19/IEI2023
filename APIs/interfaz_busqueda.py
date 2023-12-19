import tkinter as tk
from tkinter import messagebox

def abrir_interfaz_busqueda():
    contador = 0

    def mostrar_aviso():
        global contador
        contador +=1
        messagebox.showinfo("Aviso", f"Hola, este es un aviso.{contador}")

    # Crear la ventana principal
    ventana = tk.Tk()
    ventana.title("Buscador de centros educativos")

    # Establecer el tamaño inicial de la ventana (ancho x alto)
    ventana.geometry("1200x675")
    ventana.resizable(False,False)

    #Establecer etiqueta principal
    etiqueta = tk.Label(ventana, text = "Buscador de centros educativos", font=("Arial", 26))
    etiqueta.place(x=400,y=60)

    # Crear una variable de control para el menú
    variable = tk.StringVar(ventana)
    variable.set("Público")  # Opción predeterminada

    #Establecer pares etiqueta e inputText
    localidad = tk.Label(ventana, text="Localidad:", font=("Arial",16))
    localidad.place(x=300, y=120)
    localidadInput = tk.Entry(ventana)
    localidadInput.place(x=400, y=120)
    codPostal = tk.Label(ventana, text="Cod. Postal:", font=("Arial",16))
    codPostal.place(x=285, y=150)
    codPostalInput = tk.Entry(ventana)
    codPostalInput.place(x=400, y=150)
    provincia = tk.Label(ventana, text="Provincia:", font=("Arial",16))
    provincia.place(x=300, y=180)
    provinciaInput = tk.Entry(ventana)
    provinciaInput.place(x=400, y=180)
    tipo = tk.Label(ventana, text="Tipo:", font=("Arial",16))
    tipo.place(x=335, y=210)
    tipoInput = tk.OptionMenu(ventana,variable,"Público","Privado","Concertado","Otros")
    tipoInput.place(x=400,y=210)
    resultLabel = tk.Label(ventana, text="Resultados de la Busqueda:", font=("Arial",16))
    resultLabel.place(x=300, y=320)

    #Establecer botones
    cancelar = tk.Button(ventana,text="Cancelar")
    cancelar.place(x=380,y=260)
    aceptar = tk.Button(ventana,text="Aceptar")
    aceptar.place(x=480,y=260)

    #Establecer texto resultado
    resultText = tk.Text(ventana, height=15, width=110)
    resultText.place(x=200,y=350)


    #Configurar columnas
    ventana.columnconfigure(0,weight=1)
    ventana.columnconfigure(1,weight=2)
    # Iniciar el bucle de eventos
    ventana.mainloop()
