from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

url = "https://www.coordenadas-gps.com/"
driver.get(url)
direc = "CARRER JUAN XXIII 2"

time.sleep(2)

address_input = driver.find_element("id", "address")
address_input.clear()  
address_input.send_keys(direc)


button = driver.find_element(By.XPATH, "//button[contains(text(), 'Obtener Coordenadas GPS')]")
button.click()

time.sleep(4)

latitude_input = driver.find_element("id", "latitude")
longitude_input = driver.find_element("id", "longitude")

latitude = latitude_input.get_attribute("value")
longitude = longitude_input.get_attribute("value")

print("Latitude:", latitude)
print("Longitude:", longitude)

driver.quit()