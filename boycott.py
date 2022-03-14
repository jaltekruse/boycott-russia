import scrapy

class BlogSpider(scrapy.Spider):
    name = 'boycottrussia'
    start_urls = ['https://www.boycottrussia.info/top-companies']

    def parse(self, response):
        for title in response.css('.accordion-items-container'):
            for company in response.css('.accordion-item'):
                #print(company)
                yield {'company': company.css('.accordion-item__title ::text').get().strip(),
                        'details': company.css('.accordion-item__description p ::text').extract(),
                        'links': company.css('a::attr(href)').extract()
                        }
                        #            'details': company.css('.accordion-item__description ::text').get().strip(),}

                        #'details' : company.xpath("""
                        #                /div[contains(@class, 'accordion-item__description')]
                        #                /following-sibling::node()
                        #                /descendant-or-self::text()""").extract(),
                #yield {'title': title.css('::text').get()}

        #for next_page in response.css('a.next'):
            #yield response.follow(next_page, self.parse)
