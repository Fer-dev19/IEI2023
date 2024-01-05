from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class GpsScraper:
    # Método de inización para el navegador que accederá a la página web
    def setup_browser():
        # Configuración del navegador (Firefox)
        firefox_options = Options()
        firefox_options.set_preference("geo.prompt.testing", True)
        firefox_options.set_preference("geo.prompt.testing.allow", True)
        firefox_options.add_argument("--width=1920")
        firefox_options.add_argument("--height=1080")

        # Especificación de la ruta al geckodriver
        service = Service('C:/geckodriver.exe')
        driver = webdriver.Firefox(service=service, options=firefox_options)
        return driver

    # Método de iniciación para acceder a la página web
    def setup_search(driver):
        driver.get("https://www.coordenadas-gps.com/")

        # Esperar para poder aceptar las cookies de la página web
        try:
            boton_consentir = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[2]/div[1]/div[2]/div[2]/button[1]"))
            )
            boton_consentir.click()
        except Exception as e:
            print("No se pudo encontrar el botón de consentimiento de cookies:", e)
        
    # Método para calcular la longitud y latitud de un centro dada su dirección
    def search(driver, direc):
        # Localizar y esperar al cuadro de texto para introducir la dirección
        address_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "address"))
        )

        # Bajar la ventana hasta visualizar el cuadro de la dirección
        driver.execute_script("window.scrollTo(0, 600);")
        # Tiempos de espera para asegurar que la carga de los elementos haya terminado
        time.sleep(0.5)
        # Se elimina el texto que pueda tener el cuadro de texto
        address_input.clear()  
        time.sleep(0.5)
        # Se introduce la dirección del centro
        address_input.send_keys(direc)
        time.sleep(0.5)

        # Localizar y esperar hasta que el botón para que la web calcule los datos esté disponible
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Obtener Coordenadas GPS')]"))
        )

        time.sleep(0.5)
        driver.execute_script("window.scrollTo(0, 400);")
        time.sleep(0.5)
        # Se pulsa sobre el botón
        button.click()
        time.sleep(0.5)

    # Método que devuelve la latitud calculada
    def get_latitude(driver):
        # Se localiza el cuadro de texto y se espera hasta que no esté vacía
        latitude_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "latitude"))
        )
        return latitude_input.get_attribute("value")
    
    # Método que devuelve la longitud calculada
    def get_longitude(driver):
        # Se localiza el cuadro de texto y se espera hasta que no esté vacía
        longitude_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "longitude"))
        )
        return longitude_input.get_attribute("value")
