from process_parser import GenSpider


class Spider(GenSpider):
    """
    Пример генерируемого паука
    """

    def driver(self):
        """
        Путь к веб-драйверу
        :return: str
        """
        return r'C:\Users\Xorex\PycharmProjects\2gis_parser\driver\geckodriver.exe'

    def headless(self):
        """
        Установка режима безголовы
        :return: bool
        """
        return True

    def user_agent(self):
        """
        Установка юзер-агента
        :return: str
        """
        return "User-agent/6.0"

    def start_url(self):
        """
        Стартовый URL
        :return: str
        """
        return "https://2gis.ru/krasnodar/search/%D0%9F%D0%B0%D1%80%D0%B8%D0%BA%D0%BC%D0%B0%D1%85%D0%B5%D1%80%D1%81" \
               "%D0%BA%D0%B8%D0%B5/rubricId/305/filters/covid_services_home%3Bgeneral_payment_type_card%3Bbound" \
               "%3Bhas_photos%3Bhas_site%3Bbarbershop_female_haircut_starting_price%3D100%2C455 "

    def config_window_parser(self):
        """
        Конфигуратор окна. Закрытие всяких попапов, хождение по пагинации, выбор селекта детального объекта
        :return: property
        """
        self.parser.close_popup = '//*[@id="root"]/div/div/div[3]/footer/div[2]'
        self.parser.click_next_page = '//*[@id="root"]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/div[' \
                                      '2]/div[2]/div[1]/div/div/div[1]/div[3]/div[2]/div[2] '
        self.parser.select_obj_href = "div._1h3cgic > a._pbcct4"

    def export_data(self):
        """
        Выбор формата экспорта данных
        :return: str
        """
        return 'csva'

    def fetch_element(self):
        """
        Извлечение элементов
        :return: property
        """
        self.crawler.button = '//*[@class="_b0ke8"]/a'
        self.crawler.fetch_h1 = '//h1'
        self.crawler.fetch_phones = "div._49kxlr > div._b0ke8 > a._1nped2zk"
        self.crawler.fetch_emails = "div._49kxlr > div > a._1nped2zk"

    def crawler(self):
        """
        Обязательно! Вызов краулера
        :return: object class Crawl __call__
        """
        return self.crawler()


class Spider1(GenSpider):
    """
    Пример генерируемого паука
    """

    def driver(self):
        """
        Путь к веб-драйверу
        :return: str
        """
        return r'C:\Users\Xorex\PycharmProjects\2gis_parser\driver\geckodriver.exe'

    def headless(self):
        """
        Установка режима безголовы
        :return: bool
        """
        return True

    def user_agent(self):
        """
        Установка юзер-агента
        :return: str
        """
        return "User-agent/6.0"

    def start_url(self):
        """
        Стартовый URL
        :return: str
        """
        return "https://2gis.ru/krasnodar/search/%D0%91%D0%B0%D0%BD%D0%B8/filters/bound%3Bsauna_steam_type_ir_bath"

    def config_window_parser(self):
        """
        Конфигуратор окна. Закрытие всяких попапов, хождение по пагинации, выбор селекта детального объекта
        :return: property
        """
        self.parser.close_popup = '//*[@id="root"]/div/div/div[3]/footer/div[2]'
        self.parser.click_next_page = '//*[@id="root"]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/div[' \
                                      '2]/div[2]/div[1]/div/div/div[1]/div[3]/div[2]/div[2] '
        self.parser.select_obj_href = "div._1h3cgic > a._pbcct4"

    def export_data(self):
        """
        Выбор формата экспорта данных
        :return: str
        """
        return 'csv'

    def fetch_element(self):
        """
        Извлечение элементов
        :return: property
        """
        self.crawler.button = '//*[@class="_b0ke8"]/a'
        self.crawler.fetch_h1 = '//h1'
        self.crawler.fetch_phones = "div._49kxlr > div._b0ke8 > a._1nped2zk"
        self.crawler.fetch_emails = "div._49kxlr > div > a._1nped2zk"

    def crawler(self):
        """
        Обязательно! Вызов краулера
        :return: object class Crawl __call__
        """
        return self.crawler()


if __name__ == "__main__":
    s = Spider()
    s.crawler()

    # s1 = Spider1()
    # s1.crawler()