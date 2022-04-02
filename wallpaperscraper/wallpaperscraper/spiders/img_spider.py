import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy import Request
import logging
import os
import json


class ImageSpider(scrapy.Spider):
    
    name = 'wallpaper_spider'
    start_urls = ['https://wall.alphacoders.com/by_collection.php?id=81'] 
    allowed_domains = ['alphacoders.com']


    def __init__(self):
        
        # make a directory to store the wallpapers 
        try:
            print('Making directory')
            directory_name = 'Images'
            os.mkdir(directory_name)
            print('Directory successfully created!')
        except FileExistsError as e:
            print(f'Directory alread exists: {e}')    
        
    # crawler's entry point    
    def start_requests(self):
        # pages you want to fetch images from 
        for page in range(1, 4):
            next_page = f'{self.start_urls[0]}&page={str(page)}' 
            # HTTP request 
            yield Request(url=next_page, callback=self.fetch_images)
            
    
    def fetch_images(self, response):
        
        # log info
        self.logger.info('Parse function called on %s', response.url)
        print('----PARSING----')
        
        # clean the urls
        images = [image.replace('thumbbig-', '') for image in response.xpath("//img[@class='img-responsive big-thumb']/@src").getall()]
        
        # create a dictionary
        wallpaper = {
            'Page': response.url[-1], 
            'wallpapers': []
            }
        
        # loop over urls and update the dictionary
        wallpaper['wallpapers'] += [f"{str(idx)},{url}" for idx, url in enumerate(images, start=1)]
        
        # write the output into the wallpaper dictionary
        with open('Images/wallpapers.json', 'a') as json_file:
            json_file.write(json.dumps(wallpaper, indent=2))
            
# main driver
if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(ImageSpider)
    process.start()
    