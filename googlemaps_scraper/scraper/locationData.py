from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class locationData:
    SECONDS_BEFORE_MORE_REVIEWS = 0.2
    SECONDS_BEFORE_NEXT_SCROLL = 0.1
    location_data = {}
  
  # initial the locationData object
    def __init__(self, limit=10):
        self.limit = limit
        self.location_data["title"] = "NA"
        self.location_data["img"] = "NA"
        self.location_data["rating"] = "NA"
        self.location_data["reviews_count"] = "NA"
        self.location_data["address"] = "NA"
        self.location_data["phone"] = "NA"
        self.location_data["website"] = "NA"
        self.location_data["opening_hours"] = {"Monday":"NA", "Tuesday":"NA", "Wednesday":"NA", "Thursday":"NA", "Friday":"NA", "Saturday":"NA", "Sunday":"NA"}
        self.location_data["popular_times"] = {"Monday":{}, "Tuesday":{}, "Wednesday":{}, "Thursday":{}, "Friday":{}, "Saturday":{}, "Sunday":{}}
        self.location_data["reviews"] = []

    # get location data from open URL
    def get_location_data(self,driver):
    
        # get title
        try:
            title = driver.find_element(By.CSS_SELECTOR, "h1[class*='header-title']")
            self.location_data["title"] = title.text.strip()
        except:
            pass

        # get rating
        try:
            img = driver.find_element(By.CSS_SELECTOR, 'button[aria-label*="Photo"]')
            self.location_data["img"] = img.find_element(By.TAG_NAME, 'img').get_attribute('src')
        except:
            pass

        # get rating
        try:
            rating = driver.find_element(By.CLASS_NAME, "aMPvhf-fI6EEc-KVuj8d")
            self.location_data["rating"] = rating.text
        except:
            pass


        # get reviews_count
        try:
            reviews_count = driver.find_element(By.CLASS_NAME, "Yr7JMd-pane-hSRGPd")
            self.location_data["reviews_count"] = reviews_count.text.split(' ')[0].replace(',','')
        except:
            pass

        # get address
        try:
            address = driver.find_element(By.CSS_SELECTOR, "[data-item-id='address']") 
            self.location_data["address"] = address.text
        except:
            pass

        # get phone
        try:
            phone = driver.find_element(By.CSS_SELECTOR, '[data-item-id*="phone"]')
            self.location_data["phone"] = phone.text
        except:
            pass

        # get website
        try:
            website = driver.find_element(By.CSS_SELECTOR, "[data-item-id='authority']")
            self.location_data["website"] = website.text
        except:
            pass

        # get Time
        try:
            time = driver.find_element(By.CLASS_NAME,"LJKBpe-open-R86cEd-haAclf")
            time = time.get_attribute("aria-label").split('.')[0].split(';')
            
            for t in time:
                day = t.split(',')
                self.location_data["opening_hours"][day[0].strip()] = day[1].strip()
        except:
            pass

        # get popular time
        
        try:
            days_keys = {1:"Monday", 2:"Tuesday", 3:"Wednesday", 4:"Thursday", 5:"Friday", 6:"Saturday", 0:"Sunday"}
            days = driver.find_element(By.CSS_SELECTOR, 'div[aria-label*="Popular times"]').find_elements(By.CSS_SELECTOR,"div.O9Q0Ff-NmME3c-Utye1-haAclf > div")

            for i in range(len(days)):
                hours = days[i].find_elements(By.CSS_SELECTOR, '[aria-label*="busy"]')

                if len(hours) == 18:
                    for h in hours:
                        hsplit = h.get_attribute('aria-label').split('busy at')
                        key = hsplit[1].replace('.','').strip()
                        value = hsplit[0].strip()
                        self.location_data["popular_times"][days_keys[i]][key] = value

                elif self.location_data["time"][days_keys[i]] == "Closed":
                    self.location_data["popular_times"][days_keys[i]] = "Closed"
                    
                else:
                    self.location_data["popular_times"][days_keys[i]] = "Not enough data"
        except:
            pass

    # click more reviews button
    def more_reviews(self,driver):
        try:
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label*='More reviews']")))

            element = driver.find_element(By.CSS_SELECTOR, "button[aria-label*='More reviews']")
            element.click()

        except:
            print("Error on click 'More reviews' button")
            driver.quit()
            
        # wait for all reviews page to load
        time.sleep(self.SECONDS_BEFORE_MORE_REVIEWS)

    # scroll reviews page to the buttom
    def scroll_reviews(self,driver):
        
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#pane div.section-scrollbox"))) # Waits for the page to load.
            scrollable_div = driver.find_element(By.CSS_SELECTOR, "div#pane div.section-scrollbox")

            max_count = int(int(self.location_data["reviews_count"])/5)# Number of times we will scroll the scroll bar to the bottom.
            
            x = 0

            while(x<max_count):
                # It gets the section of the scroll bar.
                try:
                    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div) # Scroll it to the bottom.
                except:
                    print("Error scroll once")
                    pass

                time.sleep(self.SECONDS_BEFORE_NEXT_SCROLL) # wait for more reviews to load.
                x=x+1

        except:
            print("Error scroll")
            driver.quit()
    
    # expand all reviews
    def expand_reviews(self,driver):
        scrollable_div = driver.find_element(By.CSS_SELECTOR, "div#pane div.section-scrollbox")
        try:
            more_buttons = scrollable_div.find_elements(By.CSS_SELECTOR, 'button[aria-label*="See more"]')
            for btn in more_buttons:
                btn.click()
        except:
            print("Error expand reviews")
            driver.quit()


    # get reviews
    def get_reviews(self,driver,fileWriter,idx):
        # if reviews_count not equal to zero start scrap reviews
        if self.location_data["reviews_count"] != "0" and self.location_data["reviews_count"] != "NA":

            # click more reviews button, scroll down and expand all reviews 
            self.more_reviews(driver)
            self.scroll_reviews(driver)
            self.expand_reviews(driver)

            
            scrollable_div = driver.find_element(By.CSS_SELECTOR, "div#pane div.section-scrollbox")

            # Scrape Reviews Data
            reviews = scrollable_div.find_elements(By.CSS_SELECTOR, 'div.ODSEW-ShBeI.NIyLF-haAclf.gm2-body-2') 
            for review in reviews:
                # initial reviews_dict
                
                reviews_dict = dict()

                
                # text
                try:
                    reviews_dict['text'] = review.find_element(By.CSS_SELECTOR, 'span.ODSEW-ShBeI-text').text.strip()
                except:
                    reviews_dict['text'] = 'NA'

                # date
                try:
                    reviews_dict['date'] = review.find_element(By.CSS_SELECTOR, 'span.ODSEW-ShBeI-RgZmSc-date').text
                except:
                    reviews_dict['date'] = 'NA'

                # starts 
                try:
                    reviews_dict['starts'] = review.find_element(By.CSS_SELECTOR, 'span[aria-label*="star"]').get_attribute('aria-label').strip().split(' ')[0]
                except:
                    reviews_dict['starts'] = 'NA'


                # get reviewer_name
                try:
                    reviews_dict['reviewer_name'] = review.find_element(By.CSS_SELECTOR, 'div.ODSEW-ShBeI-title span').text
                except:
                    reviews_dict['ownreviewer_nameer'] = 'NA'

                try:
                    div_owner_nbr = review.find_element(By.CSS_SELECTOR, 'div.ODSEW-ShBeI-VdSJob').find_elements(By.TAG_NAME, 'span')
                    
                    
                    if "none" in div_owner_nbr[0].get_attribute('style'):
                        reviews_dict['is_local_guide'] = 'NO'
                        reviews_dict['reviewer_number_reviews'] = div_owner_nbr[1].text.split(' ')[0]
                    else:
                        reviews_dict['is_local_guide'] = 'YES'
                        reviews_dict['reviewer_number_reviews'] = div_owner_nbr[1].text.split(' ')[1]
                except:
                    reviews_dict['is_local_guide'] = 'NA'
                    reviews_dict['reviewer_number_reviews'] = 'NA'
                    
                
                # write file
                

                self.location_data["reviews"].append(reviews_dict)

                if self.limit < len(self.location_data["reviews"]):
                    break
            
        # if reviews_count equal to zero
        else:
            self.location_data["reviews"] = "No reviews"



