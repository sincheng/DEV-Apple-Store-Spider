import scrapy
from apple_store_spider.geocode import getCoordinates
import httplib2

def find_address(response):
    address = response.xpath('//*[@id="gallery-mapSwap-section-2"]/div[1]/div[1]/span/text()').extract()
    #Remove phone number
    address = address[:-1]
    decoded_address = list(map(lambda x:x.encode('utf-8').decode('utf-8'),address))
    return ", ".join(decoded_address)

    #//*[@id="main"]/section[3]/div/div/div[3]/div/div/p[1]
    #//*[@id="main"]/section[3]/div/div/div[3]/div/div/p[1]


class StoresSpider(scrapy.Spider):
    name = 'stores'
    allowed_domains = ['apple.com']
    start_urls = ['http://apple.com/retail/storelist//']


    def parse(self, response):
        apple_url = 'https://www.apple.com'
        #List of countries
        countries_id = response.xpath('//@data-tag').extract()
        countries = response.xpath('//*[@data-tag]/text()').extract()
        id_stores = list(map(lambda s: s + "stores", countries_id))

        for s_id, country in zip(id_stores, countries):
        #
            store = response.xpath('//*[@id="'+s_id+'"]')
        #     states = store.xpath('.//*[@class="toggle-section"]')
        #store = response.xpath('//*[@id="usstores"]')
        #states_response = store.xpath('.//*[@class="toggle"]')
            states_response = store.xpath('.//*[@class="toggle-section"]')
            states_response = ["NA"] if states_response ==[] else states_response


            for state in states_response:
                if state=="NA":
                    state_name = state
                    cities_temp = store.xpath('./div/div/div//ul/li[1]/text()').extract()
                    url_list = store.xpath('./div/div/div//ul/li/a/@href').extract()
                else:
                    state_name =  state if state == "NA" else state.xpath('./h3/text()').extract_first()
                    cities_temp = state.xpath('.//li/text()').extract()
                    url_list = state.xpath('.//li/a/@href').extract()
                cities = list(map(lambda x:x.replace(", ",""),cities_temp))
                for city , url in zip(cities, url_list):
                    store_url = apple_url + url
                    yield scrapy.Request(store_url,callback=self.parse_store , meta={'country':country,'state': state_name , 'city':city})

    def parse_store(self,response):
        store_name = response.xpath('//h1/text()').extract_first()
        img_url = response.urljoin("images/hero_medium.jpg")
        store_address = find_address(response)
        latitude = getCoordinates(store_address)[0]
        longitude = getCoordinates(store_address)[1]

        yield {
            "Country":response.meta['country'],
            "Region":response.meta['state'],
            "City":response.meta['city'],
            "Store_name":store_name.encode('utf-8').decode('utf-8'),
            "Img_url":img_url,
            "Store_address":store_address,
            "Lat":latitude,
            "Long":longitude
            }
