from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
def setup(direc):
    
    address_input = driver.find_element("id", "address")
    address_input.clear()  
    address_input.send_keys(direc)

    button = driver.find_element(By.XPATH, "//button[contains(text(), 'Obtener Coordenadas GPS')]")
    button.click()
    time.sleep(2)

def getLatitude(driver):

    latitude_input = driver.find_element("id", "latitude")

    return latitude_input.get_attribute("value")
   
def getLongitude(driver):

    longitude_input = driver.find_element("id", "longitude")

    return longitude_input.get_attribute("value")

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
url = "https://www.coordenadas-gps.com/"
driver.get(url)
time.sleep(3)
setup("CARRER JUAN XXIII 2")

latitude = getLatitude(driver)
print("Latitude:", latitude)

longitude = getLongitude(driver)

print("Longitude:", longitude)

driver.quit()