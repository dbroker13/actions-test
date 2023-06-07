from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

API_KEY = os.environ["API_KEY"]

APPIUM = 'https://dev-us-pao-5.headspin.io:7026/v0/' + API_KEY + '/wd/hub'

CAPS = {
    "deviceName": "iPhone 13",
    "udid": "00008110-000A0D823E82801E",
    'platformName': 'iOS',
    "platformVersion": "16.2",
    'automationName': 'XCUITest',
    'browserName': 'Safari',
    'headspin:capture' : True
}

driver = webdriver.Remote(
    command_executor=APPIUM,
    desired_capabilities=CAPS
)
try:
    wait = WebDriverWait(driver, 10)
    driver.get('https://the-internet.herokuapp.com')
    form_auth_link = wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Form Authentication')))
    form_auth_link.click()
    username = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#username')))
    username.send_keys('tomsmith')
    password = driver.find_element(By.CSS_SELECTOR, '#password')
    password.send_keys('SuperSecretPassword!')
    driver.find_element(By.CSS_SELECTOR, 'button[type=submit]').click()

    wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Logout'))).click()
    wait.until(EC.url_to_be('https://the-internet.herokuapp.com/login'))

    flash = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#flash')))
    assert 'logged out' in flash.text

finally:
    driver.quit()
