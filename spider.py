from processing.process_parser import GenSpider
import time
import threading


class OKna(GenSpider):
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
        return "https://2gis.ru/krasnodar/search/%D0%9E%D0%BA%D0%BD%D0%B0?m=39.016886%2C45.02984%2F16.02"

    def start_checkpoint(self):
        """
        Если нужно продолжить с точки остановки то установи флаг True
        :return:
        """
        return False

    def config_window_parser(self, parser):
        """
        Конфигурация для окна ParserGis
        :param parser: объект ParserGis
        :return: property
        """
        parser.close_popup = '//*[@id="root"]/div/div/div[3]/footer/div[2]'
        parser.click_next_page = '//*[@id="root"]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div[3]/div[2]/div[2]'
        parser.select_obj_href = "div._1h3cgic > a._pbcct4"

    def export_data(self):
        return 'db'

    def table_db(self):
        return "okna"

    def column_db(self):
        return ['name_company', 'phones', 'emails']

    def timeout(self, crawler):
        crawler.timeout_random = (0, 0)

    def fetch_element(self, crawler):
        """
        Извлекает элемент определенный по xpath
        :param crawler: объект Crawler
        :return: property
        """
        crawler.button = '//*[@class="_b0ke8"]/a'

        crawler.fetch_h1 = '//h1'
        crawler.fetch_phones = "div._49kxlr > div._b0ke8 > a._1nped2zk"
        crawler.fetch_emails = "div._49kxlr > div > a._1nped2zk"

    def __call__(self):
        return self.crawler()


class ZVod(GenSpider):
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
        return "https://2gis.ru/krasnodar/search/%D0%A7%D1%91%D1%80%D0%BD%D1%8B%D0%B9%20%D0%BC%D0%B5%D1%82%D0%B0%D0" \
               "%BB%D0%BB%D0%BE%D0%BF%D1%80%D0%BE%D0%BA%D0%B0%D1%82/rubricId/615/filters/has_photos?m=39.04778%2C45" \
               ".03613%2F16.79 "

    def start_checkpoint(self):
        """
        Если необходимо начать со старнового URL то установить флаг на False
        либо True если хотите продолжить с точки окончания сбора данных
        :return:
        """
        return False

    def config_window_parser(self, parser):
        parser.close_popup = '//*[@id="root"]/div/div/div[3]/footer/div[2]'
        parser.click_next_page = '//*[@id="root"]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div[3]/div[2]/div[2]'
        parser.select_obj_href = "div._1h3cgic > a._pbcct4"

    def export_data(self):
        return 'db'

    def table_db(self):
        return "zavod"

    def column_db(self):
        return ['name_company', 'phones', 'emails']

    def timeout(self, crawler):
        crawler.timeout_random = (0, 0)

    def fetch_element(self, crawler):
        crawler.button = '//*[@class="_b0ke8"]/a'
        crawler.fetch_h1 = '//h1'
        crawler.fetch_phones = "div._49kxlr > div._b0ke8 > a._1nped2zk"
        crawler.fetch_emails = "div._49kxlr > div > a._1nped2zk"

    def __call__(self):
        return self.crawler()


if __name__ == "__main__":

    okna = OKna()
    zavod = ZVod()

    full_time = time.time()

    p1 = threading.Thread(target=okna, daemon=True)
    p2 = threading.Thread(target=zavod, daemon=True)

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print(f"{(time.time()-full_time)/60} минуты для Всех")