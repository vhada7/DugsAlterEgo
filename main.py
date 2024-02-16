from selenium import webdriver
from selenium.webdriver.common.by import By
import time
driver = webdriver.Chrome()
driver.get("https://instagram.com")
a= driver.find_elements(By.TAG_NAME , "input")
a[0].send_keys("keepyourdamnpotato")
a[1].send_keys("Spurs1882!")
buttons = driver.find_elements(By.TAG_NAME , "button")
buttons[1].click()

time.sleep(300)
driver.close()