import pandas as pd

from random import  random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


# Download and install the Chrome driver
chrome_service = ChromeService(ChromeDriverManager().install())

# Set up options to run the driver in "headless" mode (no window)
# Comment this out if you want to see the window pop up
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument(f"--user-data-dir={userdatadir}")
# chrome_options.add_argument("profile-directory=Profile 1")
# chrome_options.add_argument('--headless')
# chrome_options.page_load_strategy = 'eager'

# Launch the driver
driver = webdriver.Chrome(options = chrome_options, service=chrome_service)
driver.get('https://accounts.spotify.com/en/login?continue=https%3A%2F%2Fcharts.spotify.com/login')


email = driver.find_element(By.ID, 'login-username')
passw = driver.find_element(By.ID, 'login-password')
login = driver.find_element(By.ID, 'login-button')

email.send_keys('<email>')
passw.send_keys('<password>')
login.click()

for d in pd.date_range(end='2023-11-22',periods=10,freq='W-THU'):
    print(d)
    
    driver.get('https://charts.spotify.com/charts/view/regional-global-weekly/'+str(d)[:10])
    time.sleep(5+random())
    downl = driver.find_element(By.CSS_SELECTOR, "a[class^='styled__CSVLink']")
    downl.click()
    time.sleep(random()*2)


driver.close()