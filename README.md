<div id="top"></div>
<div align="center">
  <h1 align="center">Google Maps Scraper</h1>
  <img src="./images/gmapscraper.png">
</div>

This Google Maps Scraper will enable you to get data from Google Places, the scraper built with Python and library <a href="https://www.selenium.dev"
  >Selenium</a>
  <br>
This scraper enables you to extract all of the following data from Google Maps:
- place title and image
- Address
- Phone and website if available
- Average rating and review count
- Opening hours
- Popular times 

The scraper also supports the scraping of all detailed information about reviews:
- Review text
- Stars
- Published date
- Reviewer name
- Reviewer number of reviews
- Reviewer is Local Guide


<!-- GETTING STARTED -->
## Installation

1. Clone the repo
   ```sh
   git clone https://github.com/mohcinsarrar/googleMaps-scraper.git
   ```
2. Install requirements
   ```sh
   pip install -r requirements.txt
   ```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

### Scrape product infos
to start scraping products from an amazon category, go to the project directory, and use this command
  ```sh
     scrapy crawl product -a category="URL" -O outputFile.csv
  ```
- outputFile.csv to save the products infos
- the URL is the link of the category page
<img src="./images/category.png">

### Scrape places
you can scrape places for a specific search query, Example : "restaurant in new york", to start scraping execute this command in the directory of the file main.py :
  ```sh
     python main.py -q "search query" -l maxPlaces -r
  ```

- -q search query : Example : "restaurant in new york"
- -l maxPlaces : max places to be scraped
- the option -r : to activate scraping of reviews
- -O outputFile.csv to save places data
- -o outputFile.csv to save reviews data

<p align="right">(<a href="#top">back to top</a>)</p>
