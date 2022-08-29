# **Blockchain Scrapers**
### Goal:
The goal of this project is to scrape relevant information from 2 blockchain related websites. I have chosen to extract article related data from www.cryptoslate.com and company record data from www.glyph.social. These websites contain a nice amount of clean blockchain related data so they are ideal candidates for scraping. I will use the Scrapy Python framework because it provides an easy way to scrape large amounts of data in a clean and comprehensible manner. The data will be stored in a MongoDB database because of its relatively effortless intergration with Scrapy. It is also a NoSQL database which is ideal for unstructured data.
### Strategy:
The strategy implemented for extracting data from these websites is as follows:
- Check the website's robots.txt file for any exposed sitemaps (They are easier to scrape).
- Since both sites have open sitemaps I will implement Scrapy's SitemapSpider to easily gather relevant urls.
- Extract all the relevant data from the urls with scrapy and xpath.
- Create a pipline that will store all items in a MongoDB Database.
- Have the raw html of each page downloaded and stored locally in a pickle format together with the url it came from. This strategy should help keep things more organized in storage while also reducing the size of each file saved.
- Export the collections from the database into a csv file using mongoexport.
- Use Pandas to read back the data gathered in the CSV files.

### Requirements:
- Python3
- MongoDB 6.0 or higher
- mongoexport

### Installation:
In the project directory:
- `pip install -r requirements.txt`

### Example Usage:
1. In the terminal, make sure you are in the blockchain_scrapers directory.
2. Startup your MongoDB database on localhost port 27017

- Crawl cryptoslate: `scrapy crawl cryptoslate`
- Crawl glyph.social: `scrapy crawl glyph_social`
- Focus crawling by category on cryptoslate: `scrapy crawl cryptoslate -a category='<desired category>'` 
- Focus crawling by company on glyphsocial: `scrapy crawl glyph_social -a company='<desired company>'` 

### Notes:
- All output is sent to the terminal and stored in the mongoDB database. You can store the yielded items in a json file by adding `-o <file name>.json` at the end of the above commands.
- A download delay of 3 seconds has been implemented for both scrapers so we don't overwhelm the sites we are scraping.
- The scrapers were designed on Windows 11 and have not been tested on Linux based systems. However, they were writen with linux systems in mind so they should run fine on them.
- Minimal data cleansing was needed in this project.
