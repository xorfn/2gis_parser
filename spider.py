from processing.process_parser import GenSpider
import time


class SpiderTest(GenSpider):
    """
    Пример генерируемого паука
    """

    def driver(self):
        return r'C:\Users\Xorex\PycharmProjects\2gis_parser\driver\chromedriver.exe'

    def headless(self):
        return True

    def user_agent(self):
        return "User-agent/6.0"


    def start_url(self):
        return "https://2gis.ru/krasnodar/search/%D0%9F%D0%B0%D1%80%D0%B8%D0%BA%D0%BC%D0%B0%D1%85%D0%B5%D1%80%D1%81%D0%BA%D0%B8%D0%B5/rubricId/305/filters/general_payment_type_card%3Bcovid_services_home%3Bbound%3Bhas_photos%3Bhas_site"

    def config_window_parser(self):
        self.parser.close_popup = '//*[@id="root"]/div/div/div[3]/footer/div[2]'
        self.parser.click_next_page = '//*[@id="root"]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div[3]/div[2]/div[2]'
        self.parser.select_obj_href = "div._1h3cgic > a._pbcct4"

    def export_data(self):
        return 'db'

    def table_db(self):
        return "barber"

    def column_db(self):
        return ['name_company', 'phones', 'emails']

    def timeout(self):
        self.crawler.timeout_random = (1, 2)

    def fetch_element(self):
        self.crawler.button = '//*[@class="_b0ke8"]/a'
        self.crawler.fetch_h1 = '//h1'
        self.crawler.fetch_phones = "div._49kxlr > div._b0ke8 > a._1nped2zk"
        self.crawler.fetch_emails = "div._49kxlr > div > a._1nped2zk"

    def __call__(self):
        return self.crawler()


if __name__ == "__main__":
    start = time.time()
    spider_test = SpiderTest()
    spider_test()
    # 4.322110811869304 минуты Firefox
    # 3.181092433134715 минуты Chrome
    print(f"{(time.time()-start)/60} минуты")


