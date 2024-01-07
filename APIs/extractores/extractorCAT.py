import sqlite3
import json

class ExtractorCAT:
    def __init__(self, db_path, json_path):
        self.db_path = db_path
        self.json_path = json_path

    def conectar_a_base_datos(self):
        return sqlite3.connect(self.db_path)

    def crear_tablas(self, conn):
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Provincia (codigo INTEGER PRIMARY KEY, nombre TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS Localidad (codigo INTEGER PRIMARY KEY, nombre TEXT, provincia INTEGER, FOREIGN KEY (provincia) REFERENCES Provincia(codigo))''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS Centro_Educativo (nombre TEXT PRIMARY KEY, tipo TEXT, direccion TEXT, codigo_postal TEXT, longitud REAL, latitud REAL, telefono TEXT, descripcion TEXT, localidad INTEGER, FOREIGN KEY (localidad) REFERENCES Localidad(codigo))''')
        conn.commit()

    def leer_archivo_json(self):
        with open(self.json_path, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)

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

            self.insertar_centro_educativo(conn, entry['denominaci_completa'], tipo_centro, entry['adre_a'], entry['codi_postal'], coordenadas_x, coordenadas_y, entry.get('telcen', None), descripcion_centro, codigo_localidad)
            lineas_procesadas += 1
        return lineas_procesadas

    def insertar_provincia(self, conn, codigo, nombre):
        cursor = conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO Provincia (codigo, nombre) VALUES (?, ?)', (codigo, nombre))
        conn.commit()

    def insertar_localidad(self, conn, codigo, nombre, provincia):
        cursor = conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO Localidad (codigo, nombre, provincia) VALUES (?, ?, ?)', (codigo, nombre, provincia))
        conn.commit()

    def insertar_centro_educativo(self, conn, nombre, tipo, direccion, codigo_postal, longitud, latitud, telefono, descripcion, localidad):
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO Centro_Educativo (nombre, tipo, direccion, codigo_postal, longitud, latitud, telefono, descripcion, localidad)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nombre, tipo, direccion, codigo_postal, longitud, latitud, telefono, descripcion, localidad))
        conn.commit()

    def obtener_tipo(self, naturaleza):
        tipo_centro = {
            'Públic': 'Público',
            'Privat': 'Privado',
            'Concertat': 'Concertado'
        }
        return tipo_centro.get(naturaleza, None)

    def ejecutar(self):
        conn = self.conectar_a_base_datos()
        try:
            self.crear_tablas(conn)
            data = self.leer_archivo_json()
            lineas_procesadas = self.procesar_datos(conn, data)
            return lineas_procesadas
        finally:
            conn.close()