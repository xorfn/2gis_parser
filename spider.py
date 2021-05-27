from process_parser import GenSpider


class SpiderApteki(GenSpider):
    """
    Пример генерируемого паука
    """

    def driver(self):
        return r'C:\Users\Xorex\PycharmProjects\2gis_parser\driver\geckodriver.exe'

    def headless(self):
        return False

    def user_agent(self):
        return "User-agent/6.0"

    def start_url(self):
        return "https://2gis.ru/krasnodar/search/%D0%90%D0%BF%D1%82%D0%B5%D0%BA%D0%B8/filters/bound%3Bhas_site%3Bhas_photos%3Bgeneral_payment_type_card%3Bwork_time%3Dtoday%2Calltime"

    def config_window_parser(self):
        self.parser.close_popup = '//*[@id="root"]/div/div/div[3]/footer/div[2]'
        self.parser.click_next_page = '//*[@id="root"]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div[4]/div[2]/div[2]'
        self.parser.select_obj_href = "div._1h3cgic > a._pbcct4"

    def export_data(self):
        return 'csv'

    def table_db(self):
        return "apteki"

    def column_db(self):
        return ['h1', 'phones', 'emails']

    def fetch_element(self):
        self.crawler.button = '//*[@class="_b0ke8"]/a'
        self.crawler.fetch_h1 = '//h1'
        self.crawler.fetch_phones = "div._49kxlr > div._b0ke8 > a._1nped2zk"
        self.crawler.fetch_emails = "div._49kxlr > div > a._1nped2zk"

    def __call__(self):
        return self.crawler()


class SpiderFitness(GenSpider):
    """
    Пример генерируемого паука
    """

    def driver(self):
        return r'C:\Users\Xorex\PycharmProjects\2gis_parser\driver\geckodriver.exe'

    def headless(self):
        return False

    def user_agent(self):
        return "User-agent/6.0"

    def start_url(self):
        return "https://2gis.ru/krasnodar/search/%D0%A4%D0%B8%D1%82%D0%BD%D0%B5%D1%81-%D0%BA%D0%BB%D1%83%D0%B1%D1%8B/rubricId/268"

    def config_window_parser(self):
        self.parser.close_popup = '//*[@id="root"]/div/div/div[3]/footer/div[2]'
        self.parser.click_next_page = '//*[@id="root"]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/div[' \
                                      '2]/div[2]/div[1]/div/div/div[1]/div[3]/div[2]/div[2] '
        self.parser.select_obj_href = "div._1h3cgic > a._pbcct4"

    def export_data(self):
        return 'csv'

    def table_db(self):
        return "fitness"

    def column_db(self):
        return ['name_company', 'phones', 'emails']

    def fetch_element(self):
        self.crawler.button = '//*[@class="_b0ke8"]/a'
        self.crawler.fetch_h1 = '//h1'
        self.crawler.fetch_phones = "div._49kxlr > div._b0ke8 > a._1nped2zk"
        self.crawler.fetch_emails = "div._49kxlr > div > a._1nped2zk"

    def __call__(self):
        return self.crawler()


if __name__ == "__main__":
    # spider_fit = SpiderFitness()
    # spider_fit()

    spider_fit = SpiderApteki()
    spider_fit()

