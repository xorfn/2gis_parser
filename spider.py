from processing.process_parser import GenSpider
import time
import threading


class SpiderParicMos(GenSpider):
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
        return "https://2gis.ru/krasnodar/search/%D0%9F%D0%B0%D1%80%D0%B8%D0%BA%D0%BC%D0%B0%D1%85%D0%B5%D1%80%D1%81%D0%BA%D0%B8%D0%B5"

    def start_checkpoint(self):
        return True

    def config_window_parser(self,parser):
        parser.close_popup = '//*[@id="root"]/div/div/div[3]/footer/div[2]'
        parser.click_next_page = '//*[@id="root"]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div[3]/div[2]/div[2]'
        parser.select_obj_href = "div._1h3cgic > a._pbcct4"

    def export_data(self):
        return 'db'

    def table_db(self):
        return "parik"

    def column_db(self):
        return ['name_company', 'phones', 'emails']

    def timeout(self):
        self.crawler.timeout_random = (0, 0)

    def fetch_element(self,crawler):
        crawler.button = '//*[@class="_b0ke8"]/a'
        crawler.fetch_h1 = '//h1'
        crawler.fetch_phones = "div._49kxlr > div._b0ke8 > a._1nped2zk"
        crawler.fetch_emails = "div._49kxlr > div > a._1nped2zk"

    def __call__(self):
        return self.crawler()

class SpiderNedvizh(GenSpider):
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
        return "https://2gis.ru/krasnodar/search/%D0%BD%D0%B5%D0%B4%D0%B2%D0%B8%D0%B6%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D1%8C"

    def start_checkpoint(self):
        return True

    def config_window_parser(self, parser):
        parser.close_popup = '//*[@id="root"]/div/div/div[3]/footer/div[2]'
        parser.click_next_page = '//*[@id="root"]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div[4]/div[2]/div[2]'
        parser.select_obj_href = "div._1h3cgic > a._pbcct4"

    def export_data(self):
        return 'db'

    def table_db(self):
        return "nedvizh"

    def column_db(self):
        return ['name_company', 'phones', 'emails']

    def timeout(self):
        self.crawler.timeout_random = (0, 0)

    def fetch_element(self, crawler):
        crawler.button = '//*[@class="_b0ke8"]/a'
        crawler.fetch_h1 = '//h1'
        crawler.fetch_phones = "div._49kxlr > div._b0ke8 > a._1nped2zk"
        crawler.fetch_emails = "div._49kxlr > div > a._1nped2zk"

    def __call__(self):
        return self.crawler()


if __name__ == "__main__":

    parik_test = SpiderParicMos()
    ned_test = SpiderNedvizh()

    full_time = time.time()

    p1 = threading.Thread(target=parik_test, daemon=True)
    p2 = threading.Thread(target=ned_test, daemon=True)

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print(f"{(time.time()-full_time)/60} минуты для Всех")