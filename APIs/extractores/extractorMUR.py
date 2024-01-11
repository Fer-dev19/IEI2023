import sqlite3
import json

class ExtractorMUR:

    #Mediante este método iniciamos el extractor
    def __init__(self, db_path, json_path):
        self.db_path = db_path
        self.json_path = json_path
        self.conn = None

    #Métodop de conexión con la BD
    def conectar_a_base_datos(self):
        self.conn = sqlite3.connect(self.db_path)

    #Método para cerrar la conexión con la BD
    def cerrar_conexion_base_datos(self):
        if self.conn:
            self.conn.close()

    #Método que crea las tablas. En caso de ya existir no lo hace
    def crear_tablas(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Provincia (
                codigo INTEGER PRIMARY KEY,
                nombre TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Localidad (
                codigo INTEGER PRIMARY KEY,
                nombre TEXT,
                provincia INTEGER,
                FOREIGN KEY (provincia) REFERENCES Provincia (codigo)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Centro_Educativo (
                nombre TEXT PRIMARY KEY,
                tipo TEXT,
                direccion TEXT,
                codigo_postal TEXT,
                longitud REAL,
                latitud REAL,
                telefono TEXT,
                descripcion TEXT,
                localidad INTEGER,
                FOREIGN KEY (localidad) REFERENCES Localidad (codigo)
            )
        ''')
        self.conn.commit()

    #Con este método insertamos todos los datos en la BD
    #Si ya existen los datos los ignora
    def insertar_datos(self, data):
        lineas_procesadas = 0
        mensaje_total = ""
        # Suponemos que la lógica de obtención del tipo de centro ya está definida en una función obtener_tipo()
        for centro in data:
            mensaje = ""
            geo_referencia = centro.get('geo-referencia', {})
            longitud = geo_referencia.get('lon', None)
            latitud = geo_referencia.get('lat', None)
            codigo_postal = centro['cpcen'] if centro['cpcen'] else None
            codigo_localidad = int(codigo_postal) if codigo_postal and codigo_postal.isdigit() else None
            cursor = self.conn.cursor()
            for clave, valor in centro.items():
                if valor is None:
                    mensaje += f"El atributo '{clave}' es null.\n"
            cursor.execute('INSERT OR IGNORE INTO Provincia VALUES (?, ?)', (30, 'Murcia'))
            cursor.execute('INSERT OR IGNORE INTO Localidad VALUES (?, ?, ?)', (codigo_localidad, centro['loccen'], 30))
            cursor.execute('''
                INSERT OR IGNORE INTO Centro_Educativo (nombre, tipo, direccion, codigo_postal, longitud, latitud, telefono, descripcion, localidad)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                centro['denLarga'] + ' ' + centro['dencen'],
                self.obtener_tipo(centro['titularidad']),
                centro['domcen'],
                codigo_postal,
                longitud,
                latitud,
                centro['telcen'],
                centro['presentacionCorta'] + ' ' + centro['web'],
                codigo_localidad
            ))
            self.conn.commit()
            mensaje_total += mensaje
            lineas_procesadas += 1
        return lineas_procesadas, mensaje_total

    #Mediante este método leemos el archivo json para posteriormente extraer los datos
    def leer_archivo_json(self):
        with open(self.json_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    #Con este método transformamos y adaptamos el tipo de colegio para el esquema global
    def obtener_tipo(self, titularidad):
        return {
            'P': 'Público',
            'N': 'Privado',
            'C': 'Concertado'
        }.get(titularidad, None)

    #Este es el método que se ejecuta desde las API para iniciar la carga
    def ejecutar(self):
        try:
            self.conectar_a_base_datos()
            self.crear_tablas()
            data = self.leer_archivo_json()
            lineas_procesadas, mensaje_error = self.insertar_datos(data)
            return lineas_procesadas, mensaje_error
        finally:
            self.cerrar_conexion_base_datos()