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
        # Tablas Provincia, Localidad y Centro_Educativo
        cursor.execute('''CREATE TABLE IF NOT EXISTS Provincia (codigo INTEGER PRIMARY KEY, nombre TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS Localidad (codigo INTEGER PRIMARY KEY, nombre TEXT, provincia INTEGER, FOREIGN KEY (provincia) REFERENCES Provincia (codigo))''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS Centro_Educativo (nombre TEXT PRIMARY KEY, tipo TEXT, direccion TEXT, codigo_postal TEXT, longitud REAL, latitud REAL, telefono TEXT, descripcion TEXT, localidad INTEGER, FOREIGN KEY (localidad) REFERENCES Localidad (codigo))''')
        self.conn.commit()

    def insertar_provincia(self, codigo, nombre):
        cursor = self.conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO Provincia VALUES (?, ?)', (codigo, nombre))
        self.conn.commit()

    def insertar_localidad(self, codigo, nombre, provincia):
        cursor = self.conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO Localidad VALUES (?, ?, ?)', (codigo, nombre, provincia))
        self.conn.commit()

    def insertar_centro_educativo(self, centro, longitud, latitud):
        cursor = self.conn.cursor()
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
            centro['CODIGO']
        ))
        self.conn.commit()

    def leer_archivo_json(self):
        with open(self.json_path, 'r', encoding='utf-8') as file:
            self.data = json.load(file)

    def obtener_tipo(self, regimen):
        return {
            'PÚB.': 'Público',
            'PRIV. CONC.': 'Concertado',
            'PRIV.': 'Privado',
            'OTROS': 'Otros'
        }.get(regimen, None)

    def procesar_datos(self):
        self.crear_tablas()
        GpsScraper.setup_search(self.driver)
        for centro in self.data:
            GpsScraper.search(self.driver, centro['TIPO_VIA']+ " " + centro['DIRECCION'] + ", " + centro['NUMERO'] + ", " + centro['CODIGO_POSTAL'] + ", " + centro['LOCALIDAD'])
            time.sleep(1)
            latitude = GpsScraper.get_latitude(self.driver)
            longitude = GpsScraper.get_longitude(self.driver)
            self.insertar_provincia(centro['CODIGO_POSTAL'][:2], centro['PROVINCIA'])
            self.insertar_localidad(centro['CODIGO_POSTAL'], centro['LOCALIDAD'], centro['CODIGO_POSTAL'][:2])
            self.insertar_centro_educativo(centro, longitude, latitude)
    
    def ejecutar(self):
        try:
            self.conectar_a_base_datos()
            self.leer_archivo_json()
            self.driver = GpsScraper.setup_browser()
            self.procesar_datos()
        finally:
            if self.driver:
                self.driver.quit()
            self.cerrar_conexion_base_datos()

    # # Lógica principal
    # ruta_db = '../baseDatos.db'
    # conn = conectar_a_base_datos(ruta_db)
    # crear_tablas(conn)
    # driver = gps_scraper.setup_browser()
    # data = leer_archivo_json('../archivosJSON/CV.json')
    # procesar_datos(conn, driver, data)
    # driver.quit()
    # cerrar_conexion_base_datos(conn)


# import sqlite3
# import json
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options

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
#         FOREIGN KEY (provincia) REFERENCES Provincia (codigo)
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
#         FOREIGN KEY (localidad) REFERENCES Localidad (codigo)
#     )
# ''')

# with open('../archivosJSON/CV.json', 'r', encoding='utf-8') as file:
#     data = json.load(file)

# def obtener_tipo(regimen):
#     if regimen == 'PÚB.':
#         return 'Público'
#     elif regimen == 'PRIV. CONC.':
#         return 'Concertado'
#     elif regimen == 'PRIV.':
#         return 'Privado'
#     elif regimen == 'OTROS':
#         return 'Otros'
#     else:
#         return None

# def searchDir(direc):
#     address_input = driver.find_element("id", "address")
#     address_input.clear()  
#     direc += ", Valencia, España"
#     address_input.send_keys(direc)
#     time.sleep(2)
#     button = driver.find_element(By.XPATH, "//button[contains(text(), 'Obtener Coordenadas GPS')]")
#     button.click()
#     time.sleep(3)

# def getLatitude(driver):
#     latitude_input = driver.find_element("id", "latitude")
#     return float(latitude_input.get_attribute("value"))
   
# def getLongitude(driver):
#     longitude_input = driver.find_element("id", "longitude")
#     return float(longitude_input.get_attribute("value"))

# options = webdriver.ChromeOptions()
# options.add_experimental_option("detach", True)
# driver = webdriver.Chrome(options=options)
# url = "https://www.coordenadas-gps.com/"
# driver.get(url)
# time.sleep(3)
# for centro in data:
#     if centro['TELEFONO'] == "" or len(centro["TELEFONO"]) != 9:
#         telefono = None
#     else: telefono = centro['TELEFONO']

#     if len(centro['CODIGO_POSTAL']) == 5:
#         codigo_postal = centro['CODIGO_POSTAL']
#     elif len(centro['CODIGO_POSTAL']) == 4:
#         codigo_postal = '0'+centro['CODIGO_POSTAL']
#     elif centro['CODIGO_POSTAL'] == None:
#         codigo_postal = None
    
#     if len(centro['CODIGO_POSTAL']) == 5:
#         codigo_provincia = centro['CODIGO_POSTAL'][:2]
#     elif len(centro['CODIGO_POSTAL']) == 4:
#         codigo_provincia = centro['CODIGO_POSTAL'][:1]
    
#     cursor.execute('INSERT OR IGNORE INTO Provincia VALUES (?, ?)', (codigo_provincia, centro['PROVINCIA']))

#     cursor.execute('INSERT OR IGNORE INTO Localidad VALUES (?, ?, ?)', (centro['CODIGO_POSTAL'], centro['LOCALIDAD'], codigo_provincia))
    
#     searchDir(centro['DIRECCION'])
#     cursor.execute('''
#         INSERT OR IGNORE INTO Centro_Educativo (nombre, tipo, direccion, codigo_postal, longitud, latitud, telefono, descripcion, localidad)
#                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
#     ''', (
#         centro['DENOMINACION'],
#         obtener_tipo(centro['REGIMEN']),
#         f"{centro['TIPO_VIA']} {centro['DIRECCION']} {centro['NUMERO']}",
#         codigo_postal,
#         getLongitude(driver),  
#         getLatitude(driver),
#         telefono,
#         f"{centro['DENOMINACION_GENERICA_ES']} {centro['DENOMINACION_GENERICA_VAL']} {centro['DENOMINACION_ESPECIFICA']} {centro['URL_ES']}",
#         centro['CODIGO']
#     ))

# driver.quit()
# conn.commit()
# conn.close()
