import scrapy
from apple_store_spider.geocode import getCoordinates

#Function to return decoded full address
def find_address(address_response):
    region= address_response.xpath('.//*[contains(@class,"region")]/text()').extract_first()
    city = address_response.xpath('.//*[contains(@class,"locality")]/text()').extract_first()
    address = address_response.xpath('.//span/text()').extract()
    #Remove phone number
    address = address[:-1]
    return region or "NA", city or "NA", ", ".join(address).encode('utf-8').decode('utf-8')

class StoresSpider(scrapy.Spider):
    name = 'stores'
    allowed_domains = ['apple.com']
    start_urls = ['http://apple.com/retail/storelist/']
    def parse(self, response):
        apple_url = 'https://www.apple.com'
        #List of countries and countries id
        countries_id = response.xpath('//@data-tag').extract()
        countries = response.xpath('//*[@data-tag]/text()').extract()
        id_list = [country_id + "stores" for country_id in countries_id]

        for s_id, country in zip(id_list, countries):
            url_list = response.xpath('//*[@id="'+s_id+'"]//ul/li/a/@href').extract()
            for store in url_list:
                store_url = apple_url + store
                yield scrapy.Request(store_url,callback=self.parse_store , meta={'country':country})

    def parse_store(self,response):
        store_name = response.xpath('//h1/text()').extract_first()
        address_response = response.xpath('//*[@id="gallery-mapSwap-section-1"]/div[2]/div[1]')
        region, city, store_address = find_address(address_response)
        img_url = response.urljoin("images/hero_medium.jpg")
        coordinates = getCoordinates(store_address)
        latitude , longitude = coordinates[0] , coordinates[1]
        yield {
            "Country":response.meta['country'],
            "Region":region,
            "City":city,
            "Name":store_name.encode('utf-8').decode('utf-8'),
            "Img":img_url,
            "Address":store_address,
            "Lat":latitude,
            "Long":longitude
            }
