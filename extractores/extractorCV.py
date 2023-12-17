import sqlite3
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def conectar_a_base_datos(ruta_db):
    return sqlite3.connect(ruta_db)

def cerrar_conexion_base_datos(conn):
    conn.close()

def crear_tablas(conn):
    cursor = conn.cursor()
    # Tablas Provincia, Localidad y Centro_Educativo
    cursor.execute('''CREATE TABLE IF NOT EXISTS Provincia (codigo INTEGER PRIMARY KEY, nombre TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Localidad (codigo INTEGER PRIMARY KEY, nombre TEXT, provincia INTEGER, FOREIGN KEY (provincia) REFERENCES Provincia (codigo))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Centro_Educativo (nombre TEXT PRIMARY KEY, tipo TEXT, direccion TEXT, codigo_postal TEXT, longitud REAL, latitud REAL, telefono TEXT, descripcion TEXT, localidad INTEGER, FOREIGN KEY (localidad) REFERENCES Localidad (codigo))''')
    conn.commit()

def insertar_provincia(conn, codigo, nombre):
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO Provincia VALUES (?, ?)', (codigo, nombre))
    conn.commit()

def insertar_localidad(conn, codigo, nombre, provincia):
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO Localidad VALUES (?, ?, ?)', (codigo, nombre, provincia))
    conn.commit()

def insertar_centro_educativo(conn, centro, longitud, latitud):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO Centro_Educativo (nombre, tipo, direccion, codigo_postal, longitud, latitud, telefono, descripcion, localidad)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        centro['DENOMINACION'],
        obtener_tipo(centro['REGIMEN']),
        f"{centro['TIPO_VIA']} {centro['DIRECCION']} {centro['NUMERO']}",
        centro['CODIGO_POSTAL'],
        longitud,  
        latitud,
        centro['TELEFONO'] if centro['TELEFONO'] and len(centro["TELEFONO"]) == 9 else None,
        f"{centro['DENOMINACION_GENERICA_ES']} {centro['DENOMINACION_GENERICA_VAL']} {centro['DENOMINACION_ESPECIFICA']} {centro['URL_ES']}",
        centro['CODIGO']
    ))
    conn.commit()

def leer_archivo_json(ruta):
    with open(ruta, 'r', encoding='utf-8') as file:
        return json.load(file)

def obtener_tipo(regimen):
    return {
        'PÚB.': 'Público',
        'PRIV. CONC.': 'Concertado',
        'PRIV.': 'Privado',
        'OTROS': 'Otros'
    }.get(regimen, None)

def configurar_navegador():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    return driver

def obtener_coordenadas(driver, direccion):
    driver.get("https://www.coordenadas-gps.com/")
    time.sleep(3)
    address_input = driver.find_element(By.ID, "address")
    address_input.clear()  
    address_input.send_keys(direccion + ", Valencia, España")
    time.sleep(2)
    button = driver.find_element(By.XPATH, "//button[contains(text(), 'Obtener Coordenadas GPS')]")
    button.click()
    time.sleep(3)
    latitude_input = driver.find_element(By.ID, "latitude")
    longitude_input = driver.find_element(By.ID, "longitude")
    return float(latitude_input.get_attribute("value")), float(longitude_input.get_attribute("value"))

def procesar_datos(conn, driver, data):
    for centro in data:
        longitud, latitud = obtener_coordenadas(driver, centro['DIRECCION'])
        insertar_provincia(conn, centro['CODIGO_POSTAL'][:2], centro['PROVINCIA'])
        insertar_localidad(conn, centro['CODIGO_POSTAL'], centro['LOCALIDAD'], centro['CODIGO_POSTAL'][:2])
        insertar_centro_educativo(conn, centro, longitud, latitud)

# Lógica principal
ruta_db = '../baseDatos.db'
conn = conectar_a_base_datos(ruta_db)
crear_tablas(conn)
driver = configurar_navegador()
data = leer_archivo_json('../archivosJSON/CV.json')
procesar_datos(conn, driver, data)
driver.quit()
cerrar_conexion_base_datos(conn)


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
