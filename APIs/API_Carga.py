from extractores.extractorCV import ExtractorCV
from extractores.extractorCAT import ExtractorCAT
from extractores.extractorMUR import ExtractorMUR
from wrappers import wrapperCSV, wrapperXML
from extractores.gps_scraper import GpsScraper
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/cargar_datos', methods=['POST'])
def cargar_datos():
    seleccion = request.json.get('seleccion')
    if not seleccion:
        return jsonify({'error': 'No se ha seleccionado ninguna comunidad'}), 400
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
    return jsonify({'mensaje': 'Datos cargados correctamente'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5003)