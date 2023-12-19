from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/buscar', methods=['GET'])
def megaMetodo():
    
    #Obtención de parámetros
    localidad = request.args.get('localidad')
    codPostal = request.args.get('codPostal')
    provincia = request.args.get('provincia')
    tipo = request.args.get('tipo')

    #Conexión a la bd
    conn = sqlite3.connect('./APIs/baseDatos.db')
    cursor = conn.cursor()

    if not (localidad or codPostal or provincia or tipo):
        return jsonify({'error': 'No se ha proporcionado ningún parámetro'}), 400 
    
    #Consulta inicial que junta las tablas
    consultaSQL = """
    SELECT CE.*, L.nombre AS nombre_localidad, P.nombre AS nombre_provincia
    FROM Centro_Educativo CE
    JOIN Localidad L ON CE.localidad = L.codigo
    JOIN Provincia P ON L.provincia = P.codigo
    WHERE 1=1
    """
    parametros = []

#Aplicación de filtros
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
    # Almacenamiento y retorno de los resultados
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
    app.run(debug=True)
