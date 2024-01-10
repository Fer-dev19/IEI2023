from extractores.extractorCV import ExtractorCV
from extractores.extractorCAT import ExtractorCAT
from extractores.extractorMUR import ExtractorMUR
from wrappers import wrapperCSV, wrapperXML
from extractores.gps_scraper import GpsScraper
from flask import Flask, request, jsonify
from flasgger import Swagger
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

SWAGGER_URL = '/swagger'
API_URL = '/static/swaggerCarga.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "API REST de carga"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

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
    lineas_procesadas = 0
    mensaje_error = ""
    for comunidad in comunidades:
        if comunidad == "Valencia":
            wrapperCSV.convertir_csv_a_json()
            extractor = ExtractorCV('./baseDatos.db', './archivosJSON/CV.json')
            lineas_procesadas, mensaje_error = extractor.ejecutar()
        elif comunidad == "Cataluña":
            wrapperXML.convertir_xml_a_json()
            extractor = ExtractorCAT('./baseDatos.db', './archivosJSON/CAT.json')
            lineas_procesadas += extractor.ejecutar()
        elif comunidad == "Murcia":
            extractor = ExtractorMUR('./baseDatos.db', './archivosJSON/MUR.json')
            lineas_procesadas += extractor.ejecutar()
    return jsonify({'lineas_procesadas':lineas_procesadas, 'mensaje_error':mensaje_error}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5003)