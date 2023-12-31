import sqlite3
import json
import time
from extractores.gps_scraper import GpsScraper

class ExtractorCV:
    def __init__(self, db_path, json_path):
        self.db_path = db_path
        self.json_path = json_path
        self.conn = None
        self.driver = None

    def conectar_a_base_datos(self):
        self.conn = sqlite3.connect(self.db_path)

    def cerrar_conexion_base_datos(self):
        if self.conn:
            self.conn.close()

    def crear_tablas(self):
        cursor = self.conn.cursor()
        # Se crean las tablas Provincia, Localidad y Centro_Educativo
        cursor.execute('''CREATE TABLE IF NOT EXISTS Provincia (codigo INTEGER PRIMARY KEY, nombre TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS Localidad (codigo INTEGER PRIMARY KEY, nombre TEXT, provincia INTEGER, FOREIGN KEY (provincia) REFERENCES Provincia (codigo))''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS Centro_Educativo (nombre TEXT PRIMARY KEY, tipo TEXT, direccion TEXT, codigo_postal TEXT, longitud REAL, latitud REAL, telefono TEXT, descripcion TEXT, localidad INTEGER, FOREIGN KEY (localidad) REFERENCES Localidad (codigo))''')
        self.conn.commit()

    def insertar_provincia(self, codigo, nombre):
        cursor = self.conn.cursor()
        # Si la provincia no está presente en la tabla, se inserta en la misma
        cursor.execute('INSERT OR IGNORE INTO Provincia VALUES (?, ?)', (codigo, nombre))
        self.conn.commit()

    def insertar_localidad(self, codigo, nombre, provincia):
        cursor = self.conn.cursor()
        # Si la localidad no está presente en la tabla, se inserta en la misma
        cursor.execute('INSERT OR IGNORE INTO Localidad VALUES (?, ?, ?)', (codigo, nombre, provincia))
        self.conn.commit()

    def insertar_centro_educativo(self, centro, longitud, latitud):
        cursor = self.conn.cursor()
        # Si el centro no está presente en la tabla, se inserta en la misma
        cursor.execute('''
            INSERT OR IGNORE INTO Centro_Educativo (nombre, tipo, direccion, codigo_postal, longitud, latitud, telefono, descripcion, localidad)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            centro['DENOMINACION'],
            self.obtener_tipo(centro['REGIMEN']),
            f"{centro['TIPO_VIA']} {centro['DIRECCION']} {centro['NUMERO']}",
            centro['CODIGO_POSTAL'],
            longitud,  
            latitud,
            centro['TELEFONO'] if centro['TELEFONO'] and len(centro["TELEFONO"]) == 9 else None,
            f"{centro['DENOMINACION_GENERICA_ES']} {centro['DENOMINACION_GENERICA_VAL']} {centro['DENOMINACION_ESPECIFICA']} {centro['URL_ES']}",
            centro['CODIGO_POSTAL']
        ))
        self.conn.commit()

    # Método para leer el archivo JSON
    def leer_archivo_json(self):
        with open(self.json_path, 'r', encoding='utf-8') as file:
            self.data = json.load(file)

    # Método para obtener el tipo del centro
    def obtener_tipo(self, regimen):
        return {
            'PÚB.': 'Público',
            'PRIV. CONC.': 'Concertado',
            'PRIV.': 'Privado',
            'OTROS': 'Otros'
        }.get(regimen, None)
    
    def acentoValencia(self, centro):
        if centro['LOCALIDAD'] == 'VALÈNCIA':
            return 'Valencia'
        else: return centro['LOCALIDAD']

    def procesar_datos(self):
        lineas_procesadas = 0
        self.crear_tablas()
        # Se llama a la clase para inicializar la búsqueda
        GpsScraper.setup_search(self.driver)

        for centro in self.data:
            # Se le introducen varios parámetros adicionales a la dirección para que la página no genere centros erróneos
            GpsScraper.search(self.driver, centro['TIPO_VIA']+ " " + centro['DIRECCION'] + ", " + centro['NUMERO'] + ", " + centro['CODIGO_POSTAL'] + ", " + centro['LOCALIDAD'])
            time.sleep(1)

            #Se obtienen los parámetros calculados por la página web
            latitude = GpsScraper.get_latitude(self.driver)
            longitude = GpsScraper.get_longitude(self.driver)

            # Se llaman a los métodos para insertar los valores en la base de datos
            self.insertar_provincia(centro['CODIGO_POSTAL'][:2], centro['PROVINCIA'])
            self.insertar_localidad(centro['CODIGO_POSTAL'], self.acentoValencia(centro), centro['CODIGO_POSTAL'][:2])
            self.insertar_centro_educativo(centro, longitude, latitude)
            lineas_procesadas += 1
        return lineas_procesadas
    
    def ejecutar(self):
        try:
            self.conectar_a_base_datos()
            self.leer_archivo_json()
            self.driver = GpsScraper.setup_browser()
            lineas_procesadas = self.procesar_datos()
            return lineas_procesadas
        finally:
            if self.driver:
                self.driver.quit()
            self.cerrar_conexion_base_datos()