import scrapy

class VGSSpider(scrapy.Spider):
    name = "vgs"
    start_urls = [
        "https://videogamesstats.com/list-of-video-game-publishers/",
    ]

    def parse(self, response):
        for pub_page in response.xpath("//li/a[starts-with(@href, 'https://videogamesstats.com/')]/@href").getall():
            if pub_page is not None:
                pub_page = response.urljoin(pub_page)
                yield scrapy.Request(pub_page, callback=self.parse_pub_page)

        """pub_page = response.xpath("//li/a[starts-with(@href, 'https://videogamesstats.com/')]/@href")[1].get()
        if pub_page is not None:
            pub_page = response.urljoin(pub_page)
            yield scrapy.Request(pub_page, callback=self.parse_pub_page)"""

        """filename = "game_publisher.html"

        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')"""

    def parse_pub_page(self, response : scrapy.http.Response):
        # print("HERE LOG", response.url)
        found_year = ""
        headquarter = ""

        try:
            found_year = response.xpath("//li/ul/li/text()")[0].get()
        except Exception:
            pass

        try:
            headquarter = response.xpath("//li/ul/li/text()")[1].get()
        except Exception:
            pass

        yield {
            "name": response.xpath("//h2[contains(@class, 'c-title')]/text()").get().replace("\n", "").replace(" Details", ""),
            "found_year": found_year,
            "headquarter": headquarter,
            "games": response.xpath("//p/strong/a/text()").getall(),
        }

"""
scrapy crawl vgs -o vgs.json
"""

class PublisherSpider(scrapy.Spider):
    name = "pub"

    start_urls = [
        "https://videogamesstats.com/Publisher/11-bit-studios/"
    ]

    def parse(self, response):
        page = response.url
        filename = "publisher_one.html"

        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')