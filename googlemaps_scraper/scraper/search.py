from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import quote_plus
import sys
import time

class search:
    SECONDS_BEFORE_SCROLL = 0.1
    SECONDS_BEFORE_NEXT_PAGE = 0.2
    # initial the driver
    def __init__(self,search=None, limit=10):
        
        if search==None:
            print("search query not defined")
            sys.exit()
        self.search = search
        self.limit = limit
        self.url = f"https://www.google.com/maps/search/{quote_plus(search)}/"
        self.places = []


    # scrape search results
    def get_search_results(self, driver):
        try:

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label*='Results for']"))) 
            scrollable_div = driver.find_element(By.CSS_SELECTOR, "div[aria-label*='Results for']")
        except:
            print('Error : the div contains result not exist')
            driver.quit()
            sys.exit()
        
        while(True):
            # scroll page to bottom
            self.scroll_to_bottom(driver)
            try:
                # get search links
                places = scrollable_div.find_elements(By.CSS_SELECTOR, "div.V0h1Ob-haAclf.OPZbO-KE6vqe.o0s21d-HiaYvf")
                
                for location in places:
                    try:
                        # get span with Ad text
                        ads = location.find_elements(By.CSS_SELECTOR, "span[class*='ARktye-Btuy5e']")
                        if len(ads) == 0:
                            self.places.append(location.find_element(By.CLASS_NAME, "a4gq8e-aVTXAb-haAclf-jRmmHf-hSRGPd").get_attribute('href'))

                        # if limit reached
                        if len(self.places)>=self.limit:
                            break
                    except:
                        pass
                
                # delete duplicate
                self.places = list(dict.fromkeys(self.places))
                
                # if limit reached
                if len(self.places)>=self.limit:
                    break
                
                # if has next page
                if not self.next_page(driver):
                    break
            except:
                pass
        

    # turn page
    def next_page(self,driver):

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label*='Next']"))) 
            next_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label*='Next']")
        except:
            print('Error : next button not exist')
            driver.quit()
            sys.exit()

        if next_button.get_attribute('disabled') is not None:
            return False

        next_button.click()
        time.sleep(self.SECONDS_BEFORE_NEXT_PAGE)
        return True

    
    def scroll_to_bottom(self,driver):
        
        try:
            # get scrollar div
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label*='Results for']"))) 
            scrollable_div = driver.find_element(By.CSS_SELECTOR, "div[aria-label*='Results for']")
            max_count = 7
            x = 0

            while(x<max_count):
                # It gets the section of the scroll bar.
                try:
                    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div) # Scroll it to the bottom.
                except:
                    print("Error scroll once")
                    pass

                time.sleep(self.SECONDS_BEFORE_SCROLL) # wait for more reviews to load.
                x += 1
        except:
            print("Error scroll")
            driver.quit()


    
