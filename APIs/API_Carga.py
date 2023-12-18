from extractores.extractorCV import ExtractorCV
from extractores.extractorCAT import ExtractorCAT
from extractores.extractorMUR import ExtractorMUR
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
        elif comunidad == "Cataluña":
            wrapperXML.convertir_xml_a_json()
            extractor = ExtractorCAT('./baseDatos.db', './archivosJSON/CAT.json')
            extractor.ejecutar()
        elif comunidad == "Murcia":
            extractor = ExtractorMUR('./baseDatos.db', './archivosJSON/MUR.json')
            extractor.ejecutar()