from scraper.driver import driver
from scraper.locationData import locationData
from scraper.search import search
import pprint
import argparse
import sys
import csv
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s : %(levelname)s : %(message)s')

# create the arguments
my_parser = argparse.ArgumentParser(description='Google Maps Scraper', 
                                    epilog='Enjoy the program! :)',
                                    allow_abbrev=False)
my_parser.add_argument('-q',
                        '--query',
                        action='store', 
                        type=str, 
                        nargs=1,
                        required=True,
                        help='the search text (Example : restaurants in new york)')

my_parser.add_argument('-l',
                        '--limit',
                        action='store', 
                        type=int, 
                        nargs=1,
                        required=True,
                        help='the max scraped places')

my_parser.add_argument('-pf',
                        '--placeFile',
                        action='store', 
                        type=str, 
                        nargs=1,
                        required=True,
                        help='file to store places data')

my_parser.add_argument('-r',
                       '--review',
                       action='store_true',
                       help='used to activate scraping reviews')

my_parser.add_argument('-rl',
                        '--reviewLimit',
                        action='store', 
                        type=int, 
                        nargs=1,
                        help='the max scraped reviews each place')

my_parser.add_argument('-rf',
                        '--reviewFile',
                        action='store', 
                        type=str, 
                        nargs=1,
                        help='file to store reviwes data')

args = my_parser.parse_args()

query = args.query[0]
maxScrapedPlaces = args.limit[0]
placeFile = args.placeFile[0]

reviewIndicator = args.review

if args.reviewLimit is not None:
    reviewLimit = int(args.reviewLimit[0])
    
else: 
    reviewLimit = args.reviewLimit

if args.reviewFile is not None:
    reviewFile = args.reviewFile[0]
    
else: 
    reviewFile = args.reviewFile
if '.csv' not in placeFile:
    print("main.py: error: file to store places data must be .csv")
    sys.exit()

if reviewIndicator:
    if reviewFile is None:
        print("main.py: error: file to store reviwes data is required")
        sys.exit()
    else:
        if '.csv' not in reviewFile:
            print("main.py: error: file to store reviwes data must be .csv")
            sys.exit()
else:
    if reviewFile is not None:
        reviewFile = None
        print("main.py: warning: scraping reviwes not active, and a file is specified !!!")
        
    
# open files function 

def open_file(path):
    return open(path, 'w', encoding='UTF8', newline='')


# create driver object and change language to english 
myDriver = driver(headless=True)
myDriver.change_google_language()

######################################################################
# create the search object
searchQuery = search(search=query, limit=maxScrapedPlaces)

# open the search page
myDriver.get_url(searchQuery.url,sleep=1)

# start scraping places
logging.info('start searching places ...')
searchQuery.get_search_results(myDriver.driver)
logging.info('end searching places ...')
######################################################################
# open files
placeHeader = ['place_id', 'title', 'img', 'rating', 'reviews_count', 'address', 'phone', 'website', 'opening_hours', 'popular_times']
placeFile = open_file(placeFile)
placeWriter = csv.writer(placeFile)
placeWriter.writerow(placeHeader)


if reviewFile is not None:
    reviewFile = open_file(reviewFile)
    reviewWriter = csv.writer(reviewFile)
    reviewHeader = ['place_id', 'text', 'date', 'starts', 'reviewer_name', 'reviewer_number_reviews', 'is_local_guide']
    reviewWriter.writerow(reviewHeader)

# parse places data
def parse_place_data(idx, location):
    placeData = []
    placeData.append(idx)
    placeData.append(location["title"])
    placeData.append(location["img"])
    placeData.append(location["rating"])
    placeData.append(location["reviews_count"])
    placeData.append(location["address"])
    placeData.append(location["phone"])
    placeData.append(location["website"])
    placeData.append(str(location["opening_hours"]))
    placeData.append(str(location["popular_times"]))

    return placeData

def parse_reviews_data(idx, location):
    placeData = []
    placeData.append(idx)
    placeData.append(location["title"])
    placeData.append(location["img"])
    placeData.append(location["rating"])
    placeData.append(location["reviews_count"])
    placeData.append(location["address"])
    placeData.append(location["phone"])
    placeData.append(location["website"])
    placeData.append(str(location["opening_hours"]))
    placeData.append(str(location["popular_times"]))

    return placeData


logging.info('start scraping places ...')
# iterate over all places links scraped with get_search_results function
places_list = []
for idx, place in enumerate(searchQuery.places):
    # create locationData object
    location = locationData(limit=reviewLimit)

    # open google maps URL
    myDriver.get_url(place)

    # start scrap data from open url
    location.get_location_data(myDriver.driver)
    logging.info('scraping place :  '+str(location.location_data['title']))
    # add location data
    placeWriter.writerow(parse_place_data(idx, location.location_data))

    # start scrap reviews
    if reviewIndicator:
        logging.info('scraping reviews for place :  '+str(location.location_data['title']))
        location.get_reviews(myDriver.driver, reviewWriter, idx)
        print(location.location_data["reviews"])
        for review in location.location_data["reviews"]:
            reviews_list = []
            reviews_list.append(idx)
            reviews_list.append(review['text'])
            reviews_list.append(review['date'])
            reviews_list.append(review['starts'])
            reviews_list.append(review['reviewer_name'])
            reviews_list.append(review['reviewer_number_reviews'])
            reviews_list.append(review['is_local_guide'])
            
            reviewWriter.writerow(reviews_list)

    places_list.append(location.location_data)

logging.info('end scraping places ...')
# close driver
myDriver.close_driver()
placeFile.close()
if reviewFile is not None:
    reviewFile.close()

