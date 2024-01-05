from flask import Flask, request, jsonify
import sqlite3
from flasgger import Swagger
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# Especificaciones para la documentación en Swagger
SWAGGER_URL = '/swagger'
API_URL = '/static/swaggerBusqueda.yaml' 
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "API de búsqueda de centros"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

 # Metodo de la API que devuelve todos los centros de la base de datos
@app.route('/getCentros', methods=['GET'])
def getCentros():

    # Conexión a la base de  datos
    conn = sqlite3.connect('./baseDatos.db')
    cursor = conn.cursor()
    
    # Definición de la consulta SQL
    consultaSQL = """
    SELECT CE.*, L.nombre AS nombre_localidad, P.nombre AS nombre_provincia
    FROM Centro_Educativo CE
    JOIN Localidad L ON CE.localidad = L.codigo
    JOIN Provincia P ON L.provincia = P.codigo
    """

    # Ejecución de la consulta sobre la base de datos
    cursor.execute(consultaSQL)

    # Almacenamiento de los resultados
    resultados = cursor.fetchall()   

    # Cierre de la conexión a la base de datos
    conn.close()

    # Almacenamiento de los resultado en una lista con los parámetros
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
        
    # Se devuelve la lista en formato JSON
    return jsonify(resultadosList)


@app.route('/buscar', methods=['GET'])
def buscar():
    
    # Obtención de los parámetros dados al llamar el método
    localidad = request.args.get('localidad')
    codPostal = request.args.get('codPostal')
    provincia = request.args.get('provincia')
    tipo = request.args.get('tipo')

    # Conexión a la base de  datos
    conn = sqlite3.connect('./baseDatos.db')
    cursor = conn.cursor()

    # Caso de error donde no se pasa ningún parámetro
    if not (localidad or codPostal or provincia or tipo):
        return jsonify({'error': 'No se ha proporcionado ningún parámetro'}), 400 
    
    # Consulta SQL por defecto
    consultaSQL = """
    SELECT CE.*, L.nombre AS nombre_localidad, P.nombre AS nombre_provincia
    FROM Centro_Educativo CE
    JOIN Localidad L ON CE.localidad = L.codigo
    JOIN Provincia P ON L.provincia = P.codigo
    WHERE 1=1
    """
    # Lista para añadir los valores de los parámetros a la consulta SQL
    parametros = []

    # Comprobación de los parámetros dados, donde se añade a la consulta por defecto 
    # que se busque el mismo proporcionado y se añade su valor a la lista previa
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

    # Ejecución de la consulta SQL con los parámetros proporcionados
    cursor.execute(consultaSQL, parametros)

    # Almacenamiento de resultados
    resultados = cursor.fetchall() 

    # Cierre de la conexión a la base de datos
    conn.close()
    
    # Almacenamiento de los resultado en una lista con los parámetros
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
        
        # Se devuelve la lista de los centros filtrados en formato JSON
        return jsonify(resultadosList)
    else:
        # Caso de error si no encuentra un centro con los parámetros dados
        return jsonify({'error': 'No se han encontrado resultados'}), 404
if __name__ == '__main__':
    app.run(debug=True, port=5004)
