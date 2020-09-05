# At the beginning we import the needed libraries. 

import requests # for making requests to the website
import lxml.html as html # for processing xml and html in Python and giving it an alias
import os # for creating directories and files
import datetime # to print datetimes

# For this project, I decided to filter the news so that I could extract those 
# on the economic section. 

HOME_URL = 'https://www.larepublica.co/' # website to scrap

# Next we have the xpath expressions, in order to filter the economic posts. 

XPATH_LINK_TO_ARTICLE = '//h2//a[@class="economiaSect"]/@href'
XPATH_TITLE = '//div[@class="row OpeningPostNormal"]//h2//a[@class="economiaSect"]/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p[not(@class)]/text()'

def parse_news(link, today):
    
    #Here we parse titles, summaries and body text of the articles to be extracted
    
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode("utf-8")
            parsed = html.fromstring(notice)

            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"','')
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                return

            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
        else:
            raise ValueError(response.status_code)
    except ValueError:
        print(ValueError)


def parse_links():

    # Here we parse the links we're going to extract

    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode("utf-8")
            parsed = html.fromstring(home)
            links_to_news = parsed.xpath(XPATH_LINK_TO_ARTICLE)

            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)

            for link in links_to_news:
                parse_news(link, today)
        else:
            raise ValueError(response.status_code)
    except ValueError:
        print(ValueError)

def run():
    parse_links()

if __name__ == '__main__':
    run()
