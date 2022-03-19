from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.options import Options as firefoxOptions
from selenium.webdriver.chrome.options import Options as chromeOptions
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager

import time


class driver:
  
  # initial the driver
  def __init__(self,headless=True):

    self.options = chromeOptions()
    if headless:
      self.options.add_argument('--headless')
    self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)


  # open that particular URL
  def get_url(self, url,sleep=10):
    try:
      self.driver.get(url) # open at the URL

    except Exception as e:
      self.driver.quit() # exit driver if errors
      return

    time.sleep(sleep) # Waiting for the page to load.

  # Closing the driver instance.
  def close_driver(self):
    self.driver.quit() 


  def change_google_language(self):

    self.get_url("https://www.google.com/preferences#languages",sleep=2)

    try:
      # get and click the english radio button
      en = self.driver.find_element(By.ID, "langten")
      en.click()

      # get and click save button
      btn = self.driver.find_element(By.ID, "form-buttons").find_element(By.CLASS_NAME, "jfk-button-action")
      btn.click()

      return True

    except:
      print("error in changing language to english")
      return False


