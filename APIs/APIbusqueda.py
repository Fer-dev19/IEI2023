from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Ruta para la búsqueda en la base de datos
@app.route('/buscarLocalidad', methods=['GET'])
def megametodo():
    # Obtener el nombre de la solicitud
    localidad = request.args.get('localidad')

    # Validar si el parámetro 'nombre' está presente
    if not localidad:
        return jsonify({'error': 'Parámetro "localidad" faltante'}), 400 
    

    # Conectar a la base de datos SQLite
    conn = sqlite3.connect('baseDatos.db')
    cursor = conn.cursor()

    # Ejecutar la consulta para obtener el elemento por nombre
    cursor.execute('SELECT * FROM Localidad WHERE LOWER(nombre) LIKE ?', ('%' + localidad.lower() + '%',))
    resultados = cursor.fetchall()

    # Cerrar la conexión a la base de datos
    conn.close()

    # Comprobar si se encontró un resultado
    if resultados:
    # Convertir las filas a una lista de diccionarios para facilitar la serialización a JSON
        resultados_list = []
        for resultado in resultados:
            resultado_dict = {
                'id': resultado[0],
                'nombre': resultado[1],
                'otro_campo': resultado[2],
            }
            resultados_list.append(resultado_dict)
        
        return jsonify(resultados_list)
    else:
        return jsonify({'error': 'Localidad no encontrada'}), 404
if __name__ == '__main__':
    app.run(debug=True)
