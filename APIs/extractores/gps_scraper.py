# 
# gps_scraper.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class GpsScraper:
    def setup_browser():
        # Configuración de Firefox
        firefox_options = Options()
        firefox_options.set_preference("geo.prompt.testing", True)
        firefox_options.set_preference("geo.prompt.testing.allow", True)
        firefox_options.add_argument("--width=1920")
        firefox_options.add_argument("--height=1080")

        # Asegúrate de especificar la ruta correcta al geckodriver
        service = Service('C:/geckodriver.exe')
        driver = webdriver.Firefox(service=service, options=firefox_options)
        return driver

    def setup_search(driver):
        driver.get("https://www.coordenadas-gps.com/")
        # Aceptar cookies
        try:
            boton_consentir = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[2]/div[1]/div[2]/div[2]/button[1]"))
            )
            boton_consentir.click()
        except Exception as e:
            print("No se pudo encontrar el botón de consentimiento de cookies:", e)
        

    def search(driver, direc):
        address_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "address"))
        )
        #driver.execute_script("arguments[0].scrollIntoView();", address_input)
        driver.execute_script("window.scrollTo(0, 600);")
        time.sleep(0.5)
        address_input.clear()  
        time.sleep(0.5)
        address_input.send_keys(direc)
        time.sleep(0.5)
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Obtener Coordenadas GPS')]"))
        )
        time.sleep(0.5)
        driver.execute_script("window.scrollTo(0, 400);")
        time.sleep(0.5)
        button.click()
        time.sleep(0.5)

    def get_latitude(driver):
        latitude_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "latitude"))
        )
        return latitude_input.get_attribute("value")
    
    def get_longitude(driver):
        longitude_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "longitude"))
        )
        return longitude_input.get_attribute("value")
