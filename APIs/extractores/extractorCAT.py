import sqlite3
import json

class ExtractorCAT:
    #inicializamos el extractor pasándole el path de la bd y de la carpeta donde se almacenarán los JSON
    def __init__(self, db_path, json_path):
        self.db_path = db_path
        self.json_path = json_path

    #Este método conecta con la base de datos mediante sqlite
    def conectar_a_base_datos(self):
        return sqlite3.connect(self.db_path)

    #Creamos las tablas en caso de que no existan
    def crear_tablas(self, conn):
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Provincia (codigo INTEGER PRIMARY KEY, nombre TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS Localidad (codigo INTEGER PRIMARY KEY, nombre TEXT, provincia INTEGER, FOREIGN KEY (provincia) REFERENCES Provincia(codigo))''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS Centro_Educativo (nombre TEXT PRIMARY KEY, tipo TEXT, direccion TEXT, codigo_postal TEXT, longitud REAL, latitud REAL, telefono TEXT, descripcion TEXT, localidad INTEGER, FOREIGN KEY (localidad) REFERENCES Localidad(codigo))''')
        conn.commit()

    #Con este método 'leemos' el json de Cataluña y lo devolvemos para utilizarlo en otro método
    def leer_archivo_json(self):
        with open(self.json_path, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)

    #Aquí se procesan los datos y se adaptan los que haya que adaptar para que coincidan con el esquema global
    #También se insertan los datos en la base de datos mediante el uso de los métodos:
        #insertar_provincia, insertar_localidad, insertar_centro_educativo
    #La variable de lineas procesadas nos devuelve las líneas insertadas en la BD.
    def procesar_datos(self, conn, data):
        lineas_procesadas = 0
        for entry in data:
            codigo_provincia = int(entry['codi_postal'][:2])
            nombre_provincia = {
                '08': 'Barcelona',
                '17': 'Girona',
                '25': 'Lleida',
                '43': 'Tarragona'
            }.get(str(codigo_provincia).zfill(2), 'Desconocida')
            
            coordenadas_x = float(entry['coordenades_geo_x']) if entry['coordenades_geo_x'] else None
            coordenadas_y = float(entry['coordenades_geo_y']) if entry['coordenades_geo_y'] else None
            codigo_localidad = int(entry['codi_municipi_6_digits'])
            
            self.insertar_provincia(conn, codigo_provincia, nombre_provincia)
            self.insertar_localidad(conn, codigo_localidad, entry['nom_municipi'], codigo_provincia)
            
            tipo_centro = self.obtener_tipo(entry['nom_naturalesa'])
            descripcion_centro = f"{entry['estudis']}, {entry['nom_titularitat']}"

            mensaje_error = self.insertar_centro_educativo(conn, entry['denominaci_completa'], tipo_centro, entry['adre_a'], entry['codi_postal'], coordenadas_x, coordenadas_y, entry.get('telcen', None), descripcion_centro, codigo_localidad)
            lineas_procesadas += 1
        return lineas_procesadas, mensaje_error

    #Inserta una provincia si no está en la BD
    def insertar_provincia(self, conn, codigo, nombre):
        cursor = conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO Provincia (codigo, nombre) VALUES (?, ?)', (codigo, nombre))
        conn.commit()

    #Inserta una localidad si no está en la BD
    def insertar_localidad(self, conn, codigo, nombre, provincia):
        cursor = conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO Localidad (codigo, nombre, provincia) VALUES (?, ?, ?)', (codigo, nombre, provincia))
        conn.commit()

    #Inserta un centro educativo si no está en la BD
    def insertar_centro_educativo(self, conn, nombre, tipo, direccion, codigo_postal, longitud, latitud, telefono, descripcion, localidad):
        cursor = conn.cursor()
        mensaje = ""
        parametros = {
            'nombre': nombre,
            'tipo': tipo,
            'direccion': direccion,
            'codigo_postal': codigo_postal,
            'longitud': longitud,
            'latitud': latitud,
            'telefono': telefono,
            'descripcion': descripcion,
            'localidad': localidad
        }

        for clave, valor in parametros.items():
            if valor is None:
                mensaje += f"El atributo '{clave}' es null.\n"
        cursor.execute('''
            INSERT OR IGNORE INTO Centro_Educativo (nombre, tipo, direccion, codigo_postal, longitud, latitud, telefono, descripcion, localidad)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nombre, tipo, direccion, codigo_postal, longitud, latitud, telefono, descripcion, localidad))
        conn.commit()
        print(mensaje)
        return mensaje

    #Mediante este método adaptamos el tipo de centro al esquema global
    def obtener_tipo(self, naturaleza):
        tipo_centro = {
            'Públic': 'Público',
            'Privat': 'Privado',
            'Concertat': 'Concertado'
        }
        return tipo_centro.get(naturaleza, None)

    #Este es el método que se ejecutará desde la API para iniciar la extracción
    def ejecutar(self):
        conn = self.conectar_a_base_datos()
        try:
            self.crear_tablas(conn)
            data = self.leer_archivo_json()
            lineas_procesadas, mensaje_error = self.procesar_datos(conn, data)
            return lineas_procesadas, mensaje_error
        finally:
            conn.close()