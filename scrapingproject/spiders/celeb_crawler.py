import scrapy
import string


class CelebCrawlerSpider(scrapy.Spider):
    name = 'celeb-crawler'
    allowed_domains = ['en.wikipedia.org']
    celebs = [
       "Nicki Minaj",
"Elizabeth Hurley",
"Dwayne_Johnson",
"Maude Apatow",
"Latto",
"Addison Rae",
"Olivia Rodrigo",
"Kim Petras",
"Storm Reid",
"Bella Thorne",


    ]
    start_urls = ["https://en.wikipedia.org/wiki/"+x for x in celebs]

    def parse(self, response):
        nickname_selector = "//th[@class='infobox-above']/div/text()"
        full_name_selector = "//td[@class='infobox-data']/div[@class='nickname']/text()"
        b_day_selector = "//td[@class='infobox-data']/text()"
        birth_place_selector = "//td[@class='infobox-data']/div[@class='birthplace']//text()"
        year_active_selector = "//*[contains(text(),'Years') and contains(text(),'active')]//parent::node()//td//text()"
        occupation_selector = "//th[contains(text(),'Occupation')]//parent::node()//li//text()"
        occupation_selector_2 = "//th[contains(text(),'Occupation')]//parent::node()//td//text()"

        nick_name = response.xpath(nickname_selector).get()
        full_name = response.xpath(full_name_selector).get()

        if full_name==None:
            full_name = nick_name

        b_day = response.xpath(b_day_selector).get()
        birth_place = "".join(response.xpath(birth_place_selector).getall(
        ))

        year_active_temp=response.xpath(year_active_selector).getall()
        if len(year_active_temp) >1 and "present" not in year_active_temp[0]:
            year_active_selector="//*[contains(text(),'Years') and contains(text(),'active')]//parent::node()//td//*[not(self::style)]//text()";
            years_active =", ".join(response.xpath(year_active_selector).getall())
        else:
            years_active = response.xpath(year_active_selector).get()
         
        
        if years_active==None:
            year_active_selector="//*[contains(text(),'Years') and contains(text(),'active')]//parent::node()//parent::node()//td//text()"
            years_active = response.xpath(year_active_selector).get()

        


        occupation = response.xpath(occupation_selector).getall()
        if len(occupation) == 0:
            occupation = response.xpath(occupation_selector_2).getall()

        occupations = ', '.join(occupation)

        result = {
            "nickname": nick_name,
            "full_name": full_name,
            "b_day": b_day,
            "birth_place": birth_place,
            "years_active": years_active,
            "occupation": string.capwords(occupations),
            "wiki_url": response.request.url,
        }
        # resultt = [full_name, b_day, birth_place, years_active, occupations]
        yield result
