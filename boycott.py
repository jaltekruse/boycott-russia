import scrapy
import re

class BlogSpider(scrapy.Spider):
    name = 'boycottrussia'
    start_urls = ['https://www.boycottrussia.info/top-companies']

    def parse(self, response):
        for section in response.css('section'):
            sector = section.css('h3 ::text').extract()
            if (sector):
                sector = sector[0].replace('Companies in the','').replace('Companies in','').strip()
            for company in section.css('.accordion-item'):
                #print(company)
                company_name = company.css('.accordion-item__title ::text').get()
                details = company.css('.accordion-item__description p ::text').extract()
                details = str(details)
                find_country = re.search('Country:([^,]*)\',', details, re.IGNORECASE)
                if (find_country):
                    country = find_country.group(1).strip()
                find_ceo = re.search('CEO:([^,]*)\',', details, re.IGNORECASE)
                if (find_ceo):
                    ceo = find_ceo.group(1).strip()
                find_cfo = re.search('CFO:([^,]*)\',', details, re.IGNORECASE)
                if (find_cfo):
                    cfo = find_cfo.group(1).strip()
                yield {'company': company_name.replace('☑️', '').replace('❌', '').strip(),
                        'sector': sector,
                        'country' : country,
                        'ceo' : ceo,
                        'cfo' : cfo,
                        'action': company_name.strip().endswith('☑️'),
                        'no_action': company_name.strip().endswith('❌'),
                        'details': details,
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
