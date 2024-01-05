from flask import Flask, request, jsonify
import sqlite3
from flasgger import Swagger
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

SWAGGER_URL = '/swagger'
API_URL = '/static/swaggerBusqueda.yaml' 
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "API de búsqueda de centros"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/getCentros', methods=['GET'])
def getCentros():

    conn = sqlite3.connect('./baseDatos.db')
    cursor = conn.cursor()
    
    consultaSQL = """
    SELECT CE.*, L.nombre AS nombre_localidad, P.nombre AS nombre_provincia
    FROM Centro_Educativo CE
    JOIN Localidad L ON CE.localidad = L.codigo
    JOIN Provincia P ON L.provincia = P.codigo
    """
    cursor.execute(consultaSQL)
    resultados = cursor.fetchall()   
    conn.close()

    if resultados:
        resultadosList = []
        for resultado in resultados:
            resultadoDict = {
                'nombre': resultado[0],
                'tipo': resultado[1],
                'direccion': resultado[2],
                'codigo_postal': resultado[3],
                'longitud': resultado[4],
                'latitud': resultado[5],
                'telefono': resultado[6],
                'descripcion': resultado[7],
                'localidad': resultado[9],
                'provincia': resultado[10]
            }
            resultadosList.append(resultadoDict)
        
    return jsonify(resultadosList)


@app.route('/buscar', methods=['GET'])
def megaMetodo():
    
    localidad = request.args.get('localidad')
    codPostal = request.args.get('codPostal')
    provincia = request.args.get('provincia')
    tipo = request.args.get('tipo')

    conn = sqlite3.connect('./baseDatos.db')
    cursor = conn.cursor()

    if not (localidad or codPostal or provincia or tipo):
        return jsonify({'error': 'No se ha proporcionado ningún parámetro'}), 400 
    
    consultaSQL = """
    SELECT CE.*, L.nombre AS nombre_localidad, P.nombre AS nombre_provincia
    FROM Centro_Educativo CE
    JOIN Localidad L ON CE.localidad = L.codigo
    JOIN Provincia P ON L.provincia = P.codigo
    WHERE 1=1
    """
    parametros = []

    if localidad:
        consultaSQL += " AND LOWER(L.nombre) LIKE ?"
        parametros.append('%' + localidad.lower() + '%') 
    if codPostal:
        consultaSQL += " AND CE.codigo_postal LIKE ?"
        parametros.append('%' + codPostal + '%')

    if provincia:
        consultaSQL += " AND LOWER(P.nombre) LIKE ?"
        parametros.append('%' + provincia.lower() + '%')

    if tipo:
        consultaSQL += " AND CE.tipo = ?"
        parametros.append(tipo)    

    cursor.execute(consultaSQL, parametros)
    resultados = cursor.fetchall()   
    conn.close()
    
    if resultados:
        resultadosList = []
        for resultado in resultados:
            resultadoDict = {
                'nombre': resultado[0],
                'tipo': resultado[1],
                'direccion': resultado[2],
                'codigo_postal': resultado[3],
                'longitud': resultado[4],
                'latitud': resultado[5],
                'telefono': resultado[6],
                'descripcion': resultado[7],
                'localidad': resultado[9],
                'provincia': resultado[10]
            }
            resultadosList.append(resultadoDict)
        
        return jsonify(resultadosList)
    else:
        return jsonify({'error': 'No se han encontrado resultados'}), 404
if __name__ == '__main__':
    app.run(debug=True, port=5004)
