import sqlite3
import json

class ExtractorCAT:
    def __init__(self, db_path, json_path):
        self.db_path = db_path
        self.json_path = json_path
        self.conn = None

    def conectar_a_base_datos(self):
        self.conn = sqlite3.connect(self.db_path)

    def cerrar_conexion_base_datos(self):
        if self.conn:
            self.conn.close()

    def crear_tablas(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Provincia (codigo INTEGER PRIMARY KEY, nombre TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS Localidad (codigo INTEGER PRIMARY KEY, nombre TEXT, provincia INTEGER, FOREIGN KEY (provincia) REFERENCES Provincia (codigo))''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS Centro_Educativo (nombre TEXT PRIMARY KEY, tipo TEXT, direccion TEXT, codigo_postal TEXT, longitud REAL, latitud REAL, telefono TEXT, descripcion TEXT, localidad INTEGER, FOREIGN KEY (localidad) REFERENCES Localidad (codigo))''')
        self.conn.commit()

    def leer_archivo_json(self):
        with open(self.json_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def insertar_provincia(self, codigo, nombre):
        cursor = self.conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO Provincia (codigo, nombre) VALUES (?, ?)', (codigo, nombre))
        self.conn.commit()

    def insertar_localidad(self, codigo, nombre, provincia):
        cursor = self.conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO Localidad (codigo, nombre, provincia) VALUES (?, ?, ?)', (codigo, nombre, provincia))
        self.conn.commit()

    def insertar_centro_educativo(self, centro):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO Centro_Educativo (nombre, tipo, direccion, codigo_postal, longitud, latitud, telefono, descripcion, localidad)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            centro['denominaci_completa'],
            centro['tipo'],
            centro['direccion'],
            centro['codigo_postal'],
            centro['longitud'],
            centro['latitud'],
            centro['telefono'],
            centro['descripcion'],
            centro['localidad']
        ))
        self.conn.commit()

    def procesar_datos(self, data):
        for centro in data:
            # Aquí asumimos que la estructura del JSON es la misma que en tu ejemplo
            codigo_provincia = centro['codigo_provincia']
            nombre_provincia = centro['nombre_provincia']
            self.insertar_provincia(codigo_provincia, nombre_provincia)

            codigo_localidad = centro['codigo_localidad']
            nombre_localidad = centro['nombre_localidad']
            self.insertar_localidad(codigo_localidad, nombre_localidad, codigo_provincia)

            # Convertimos el centro a un diccionario con nombres de campo que coincidan con los parámetros de insertar_centro_educativo
            centro_dict = {
                'denominaci_completa': centro['nombre'],
                'tipo': centro['tipo'],
                'direccion': centro['direccion'],
                'codigo_postal': centro['codigo_postal'],
                'longitud': centro['longitud'],
                'latitud': centro['latitud'],
                'telefono': centro['telefono'],
                'descripcion': centro['descripcion'],
                'localidad': codigo_localidad
            }
            self.insertar_centro_educativo(centro_dict)

    def ejecutar(self):
        try:
            self.conectar_a_base_datos()
            self.crear_tablas()
            data = self.leer_archivo_json()
            self.procesar_datos(data)
        finally:
            self.cerrar_conexion_base_datos()

# Ejemplo de uso de la clase ExtractorCAT:
# extractor_cat = ExtractorCAT('ruta/a/la/base/de/datos.db', 'ruta/al/archivo/CAT.json')
# extractor_cat.ejecutar()


# Puedes usar esta clase desde cualquier lugar de tu código así:
# extractor_cat = ExtractorCAT('../baseDatos.db', '../archivosJSON/CAT.json')
# extractor_cat.ejecutar()


# import sqlite3
# import json

# conn = sqlite3.connect('../baseDatos.db')
# cursor = conn.cursor()

# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS Provincia (
#         codigo INTEGER PRIMARY KEY,
#         nombre TEXT
#     )
# ''')

# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS Localidad (
#         codigo INTEGER PRIMARY KEY,
#         nombre TEXT,
#         provincia INTEGER,
#         FOREIGN KEY (provincia) REFERENCES Provincia(codigo)
#     )
# ''')

# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS Centro_Educativo (
#         nombre TEXT PRIMARY KEY,
#         tipo TEXT,
#         direccion TEXT,
#         codigo_postal TEXT,
#         longitud REAL,
#         latitud REAL,
#         telefono TEXT,
#         descripcion TEXT,
#         localidad INTEGER,
#         FOREIGN KEY (localidad) REFERENCES Localidad(codigo)
#     )
# ''')

# def insert_provincia(codigo, nombre):
#     cursor.execute('INSERT OR IGNORE INTO Provincia (codigo, nombre) VALUES (?, ?)', (codigo, nombre))

# def insert_localidad(codigo, nombre, provincia):
#     cursor.execute('INSERT OR IGNORE INTO Localidad (codigo, nombre, provincia) VALUES (?, ?, ?)', (codigo, nombre, provincia))

# def insert_centro_educativo(nombre, tipo, direccion, codigo_postal, longitud, latitud, telefono, descripcion, localidad):
#     cursor.execute('''
#         INSERT OR IGNORE INTO Centro_Educativo (nombre, tipo, direccion, codigo_postal, longitud, latitud, telefono, descripcion, localidad)
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
#     ''', (nombre, tipo, direccion, codigo_postal, longitud, latitud, telefono, descripcion, localidad))

# with open('../archivosJSON/CAT.json', 'r', encoding='utf-8') as json_file:
#     data = json.load(json_file)

#     for entry in data:
#         codigo_provincia = int(entry['codi_postal'][:2])
#         nombre_provincia = {
#             '8': 'Barcelona',
#             '17': 'Girona',
#             '25': 'Lleida',
#             '43': 'Tarragona'
#         }.get(str(codigo_provincia), 'Desconocida')

#         if entry['coordenades_geo_x'] == None:
#             coordenadas_x = None
#         else:
#             coordenadas_x = float(entry['coordenades_geo_x'])
        
#         if entry['coordenades_geo_y'] == None:
#             coordenadas_y = None
#         else:
#             coordenadas_y = float(entry['coordenades_geo_y'])

#         codigo_localidad = int(entry['codi_municipi_6_digits']) if len(entry['codi_municipi_6_digits']) == 6 else int('0' + entry['codi_municipi_6_digits'][:5])

#         insert_provincia(codigo_provincia, nombre_provincia)
#         insert_localidad(codigo_localidad, entry['nom_municipi'], codigo_provincia)

#         if entry['nom_naturalesa'] == 'Públic':
#             tipo_centro = 'Público'
#         elif entry['nom_naturalesa'] == 'Privat':
#             tipo_centro = 'Privado'
#         else: tipo_centro = None
#         descripcion_centro = f"{entry['estudis']}, {entry['nom_titularitat']}"

#         insert_centro_educativo(
#             entry['denominaci_completa'],
#             tipo_centro,
#             entry['adre_a'],
#             entry['codi_postal'],
#             coordenadas_x,
#             coordenadas_y,
#             None,
#             descripcion_centro,
#             codigo_localidad
#         )

# conn.commit()
# conn.close()
