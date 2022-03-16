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
                company_name = company.css('.accordion-item__title ::text').get()
                details = company.css('.accordion-item__description p ::text').extract()
                company_info = {}
                for detail in details:
                    find_labeled_val = re.search('^([^:]*):([^,]*)', detail.strip(), re.IGNORECASE)
                    if (find_labeled_val):
                        label = find_labeled_val.group(1).strip().lower()
                        if (label in ['country', 'ceo','cfo']):
                            company_info[label] = find_labeled_val.group(2).strip()
                        else:
                            company_info['other'] = detail.strip()

                if (not 'other' in company_info):
                    company_info['other'] = '-'

                links = company.css('a')
                if (links):
                    website = links[0].css('::attr(href)').extract()[0]
                    link_label = links[0].css('::text').extract()[0]
                    if (link_label.strip().lower() != 'website'):
                        raise Exception(company_name + ' fist link was not labeled website, it was labeled: ' + link_label)
                    if (len(links.getall()) > 2):
                        raise Exception(company_name + ' had more than 2 links')

                    twitter = ''
                    if (len(links.getall()) == 2):
                        link_label = links[1].css('::text').extract()[0]
                        if (link_label.strip().lower() != 'twitter'):
                            raise Exception(company_name + ' fist link was not labeled twitter, it was labeled: ' + link_label)
                        twitter = links[1].css('::attr(href)').extract()[0]

                    if (twitter and (not ('twitter' in twitter))):
                        raise Exception(company_name + ' second link was not for twitter ' + twitter)

                    twitter_handle = ''
                    if (twitter):
                        find_handle = re.search('.*twitter.com/([^?]*).*', twitter, re.IGNORECASE)
                        if (find_handle):
                            twitter_handle = find_handle.group(1).strip()
                company_info.update({'company': company_name.replace('☑️', '').replace('❌', '').strip(),
                        'sector': sector,
                        'action': company_name.strip().endswith('☑️'),
                        'no_action': company_name.strip().endswith('❌'),
                        'website': website,
                        'twitter': twitter,
                        'twitter_handle': twitter_handle,
                        'details': details
                        })
                yield company_info
                        #            'details': company.css('.accordion-item__description ::text').get().strip(),}

                        #'details' : company.xpath("""
                        #                /div[contains(@class, 'accordion-item__description')]
                        #                /following-sibling::node()
                        #                /descendant-or-self::text()""").extract(),
                #yield {'title': title.css('::text').get()}

        #for next_page in response.css('a.next'):
            #yield response.follow(next_page, self.parse)
