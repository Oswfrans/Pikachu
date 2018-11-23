import pandas as pd
import requests
import io

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy import log

#import correct crawler here
#https://github.com/tvl/scrapy-oddsportal/tree/master/oddsportal
from testspiders.spiders.followall import FollowAllSpider

#SPI data
spi_url= "https://projects.fivethirtyeight.com/soccer-api/club/spi_matches.csv"

r = requests.post(spi_url,data=params)

if r.ok:
    data = r.content.decode('utf8')
    df = pd.read_csv(io.StringIO(data))

print(df.head())

#Oddsportal data

spider = FollowAllSpider(domain='scrapinghub.com')
crawler = Crawler(Settings())
crawler.configure()
crawler.crawl(spider)
crawler.start()
log.start()
reactor.run() # the script will block here
