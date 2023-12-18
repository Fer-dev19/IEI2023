from extractores.extractorCV import ExtractorCV
from extractores.gps_scraper import GpsScraper
from wrappers import wrapperCSV, wrapperXML

def cargar_datos(seleccion):
    #Si se selecciona la opción "Cargar Todas"
    if "Seleccionar todas" in seleccion:
        comunidades = ["Valencia", "Cataluña", "Murcia"]
    else:
        comunidades = seleccion

    for comunidad in comunidades:
        if comunidad == "Valencia":
            wrapperCSV.convertir_csv_a_json()
            extractor = ExtractorCV('./baseDatos.db', './archivosJSON/CV.json')
            extractor.ejecutar()

cargar_datos(["Valencia"])