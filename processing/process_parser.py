import os
import random
import sys
import time
import threading, queue

from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from models.sqlite import SqliteDb
from processing.export_data import ExportData

sys.setrecursionlimit(20000)


# Скачать web_driver
# https://github.com/mozilla/geckodriver/releases
# https://sites.google.com/chromium.org/driver/downloads

class Driver:
    """

    """
    options = webdriver.ChromeOptions()
    user_agent = None
    path_dir = None

    def __init__(self):
        self.queue = queue.Queue()
        self._driver = self.web_driver()

    def web_driver(self):
        """

        :return:
        """
        if os.path.exists(self.path_dir):
            return webdriver.Chrome(
                executable_path=self.path_dir,
                chrome_options=self.options)
        else:
            raise FileExistsError(f"Не найден web_driver на пути {self.path_dir}")


class ParserGis(Driver, SqliteDb):
    def __init__(self):
        self._url = None
        self._close_popup = None
        self._click_next_page = None
        self._select_obj_href = None
        self._data_base = None
        self._config_table_urls = None
        super().__init__()
        SqliteDb.__init__(self)

    @property
    def config_table_urls(self):
        return self._config_table_urls

    @config_table_urls.setter
    def config_table_urls(self, value):
        if self._config_table_urls is None:
            self._config_table_urls = value

    @property
    def close_popup(self):
        return self._close_popup

    @close_popup.setter
    def close_popup(self, value):
        if self._close_popup is None:
            self._close_popup = value

    @property
    def click_next_page(self):
        return self._click_next_page

    @click_next_page.setter
    def click_next_page(self, value):
        if self._click_next_page is None:
            self._click_next_page = value

    @property
    def select_obj_href(self):
        return self._select_obj_href

    @select_obj_href.setter
    def select_obj_href(self, value):
        if self._select_obj_href is None:
            self._select_obj_href = value

    @property
    def start_url(self):
        return self._url

    @start_url.setter
    def start_url(self, value):
        if self._url is None:
            self._url = value
            self.execute_parser()

    @property
    def data_base(self):
        return self._data_base

    @data_base.setter
    def data_base(self, value):
        if self._data_base is None:
            self._data_base = value

    def close_popup_cookies(self):
        """

        :return:
        """
        try:
            self._driver.find_element_by_xpath(self._close_popup).click()
        except NoSuchElementException:
            print(f"Элемента нет")

    def execute_parser(self):
        """

        :return:
        """
        try:
            self._driver.get(self._url)
            print(f"Запущено: {self._url}")
        except Exception as e:
            print(f"Что-то пошло не так: {e}")

        self.close_popup_cookies()

    def __parser(self):
        """

        :return:
        """
        time.sleep(random.randint(2, 6))
        href = self._driver.find_elements_by_css_selector(self._select_obj_href)

        for elem in href:
            self.queue.put(elem.get_attribute('href').split("?")[0])

    def run_parser(self, next_page=True):
        """

        :param next_page:
        :return:
        """
        self.__parser()
        if next_page:
            self.__next_pages()
        else:
            print(f"Собрано ссылок {self.queue.qsize()}")
            if self._data_base == "db":
                self.create_data_urls(list(self.queue.queue), self._config_table_urls)
            else:
                print("Неверная операция")
            return self.queue

    def __next_pages(self):
        """

        :return:
        """
        if "2gis" in self._driver.current_url:
            try:
                self._driver.find_element_by_xpath(self._click_next_page).click()
                self.run_parser()
            except NoSuchElementException:
                self.run_parser(next_page=False)
                self._driver.close()
                self._driver.quit()

    @property
    def queue_exp(self):
        return self.queue.qsize()


class Crawl(Driver, ExportData):
    def __init__(self, links, export=None, config_table=None):
        self._links = links
        self.export = export
        self.config_table = config_table
        self._timeout_random = None
        self._click_more_phone = None
        self._fetch_h1 = None
        self._fetch_phones = None
        self._fetch_emails = None
        self.threadLocal = threading.local()
        super().__init__()
        SqliteDb.__init__(self)

    @property
    def name_db(self):
        return self.db_name

    @property
    def links(self):
        return self._links

    @property
    def fetch_h1(self):
        return self._fetch_h1

    @property
    def fetch_phones(self):
        return self._fetch_phones

    @property
    def fetch_emails(self):
        return self._fetch_emails

    @property
    def button(self):
        return self._click_more_phone

    @property
    def timeout_random(self):
        return self._timeout_random

    @timeout_random.setter
    def timeout_random(self, value):
        if isinstance(value, tuple):
            self._timeout_random = value
        else:
            raise TypeError("Тип данных для timeout_random должен быть контеж пример: (1,2)")

    @links.setter
    def links(self, value):
        self._links = value

    @name_db.setter
    def name_db(self,value):
         self.db_name = value

    @button.setter
    def button(self, value):
        if self._click_more_phone is None:
            self._click_more_phone = value

    @fetch_h1.setter
    def fetch_h1(self, value):
        if self._fetch_h1 is None:
            self._fetch_h1 = value

    @fetch_phones.setter
    def fetch_phones(self, value):
        if self._fetch_phones is None:
            self._fetch_phones = value

    @fetch_emails.setter
    def fetch_emails(self, value):
        if self._fetch_emails is None:
            self._fetch_emails = value

    def collect_data(self, h1, phone, email):
        """

        :param h1:
        :param phone:
        :param email:
        :return:
        """
        name = self._driver.find_element_by_xpath(h1).text
        phones = self._driver.find_elements_by_css_selector(phone)
        emails = self._driver.find_elements_by_css_selector(email)
        return name, phones, emails


    def execute_crawler(self, links):
        """

        :param links:
        :return:
        """
        while True:
            print(links.qsize())
            link = links.get()
            self._driver.get(link)

            if self.timeout_random is not None:
                time.sleep(random.randint(*self.timeout_random))

            try:
                click_more_phone = self._driver.find_element_by_xpath(self._click_more_phone)
                self._driver.execute_script("arguments[0].click();", click_more_phone)
            except NoSuchElementException:
                print("Нет элемента для клика click_more_phone")

            h1, phones, emails = self.collect_data(self._fetch_h1, self._fetch_phones, self._fetch_emails)
            try:
                self._export_to(link, h1, phones, emails, type_format=self.export, config_table=self.config_table)
            except ValueError as e:
                print(e)
                self._driver.close()
                self._driver.quit()
                break
            else:
                links.task_done()

            if links.empty():
                print(f"Создан фаил 2gis.{self.export}")
                self._driver.close()
                self._driver.quit()
                break

    def __call__(self, *args, **kwargs):
        """

        :return:
        """
        threading.Thread(target=self.execute_crawler, args=(self._links,), daemon=True).start()
        self._links.join()

        print("Все объекты обработаны")


class GenSpider(ABC):
    """

    """
    def __init__(self):
        Driver.path_dir = self.driver()
        Driver.options.headless = self.headless()
        Driver.options.add_argument(f"user-agent={self.user_agent()}")

        # создаем объект классов для конфирурации запуска
        self.__config_abc()

    def __config_abc(self):
        self.queue_checkpoint = queue.Queue()
        self.sqlite_mod = SqliteDb()

        if not self.start_checkpoint():
            self.parser = ParserGis()
            self.parser.settings = self.config_window_parser(self.parser)
            self.parser.start_url = self.start_url()
            if self.export_data() == "db":
                self.parser.config_table_urls = self.__config_table()
                self.parser.data_base = self.export_data()
            self.parser.run_parser()

            # создаем объект Crawler для конфирурации запуска
            self.crawler = self.__crawler(queue_links=self.parser.queue)
        else:
            self.crawler = self.__crawler(queue_links=self.__checkpoint(self.__config_table()))
        self.timeout()
        self.fetch_element(self.crawler)


    @abstractmethod
    def driver(self):
        """
        Путь к веб-драйверу
        :return: str
        """

    @abstractmethod
    def headless(self):
        """
        Установка режима безголовы
        :return: bool
        """
        return True

    @abstractmethod
    def user_agent(self):
        """
        Установка юзер-агента
        :return: str
        """
    @abstractmethod
    def timeout(self):
        """
        Таймаут модуля рандом
        :return: tuple
        """
    @abstractmethod
    def start_url(self):
        """
        Стартовый URL
        :return: str
        """

    @abstractmethod
    def start_checkpoint(self):
        """
        Сробатывает сбор данных с точки остановки класса Crawler (не работает для ParserGis)
        Соберет неизвлеченные данные по URL
        :return:
        """

    @abstractmethod
    def config_window_parser(self, parser):
        """
        Конфигуратор окна для ParserGis. Закрытие всяких попапов, хождение по пагинации, выбор селекта детального объекта
        :return: property
        """

    def table_db(self):
        """
        Название таблтцы БД
        :return:
        """

    def column_db(self):
        """
        Столбцы базы первичный ключ создается на уровень ниже
        :return:
        """

    @abstractmethod
    def export_data(self):
        """
        Выбор формата экспорта данных
        :return: str
        """

    def __checkpoint(self, config_table):
        """

        :param config_table:
        :return:
        """
        name_table, column = config_table

        sql = f"""select url from {name_table} WHERE {column[0]} is NULL"""

        res = self.sqlite_mod.execute_db(sql)
        for item in res:
            self.queue_checkpoint.put(item[0])

        return self.queue_checkpoint

    def __config_table(self):
        """

        :return:
        """
        if self.export_data() == "db":
            return self.table_db(), self.column_db()

    def __crawler(self, queue_links):
        """

        :param qlinks:
        :return:
        """
        return Crawl(queue_links, export=self.export_data(), config_table=self.__config_table())

    @abstractmethod
    def fetch_element(self, crawler):
        """
        Извлечение элементов
        :return: property
        """

    @abstractmethod
    def __call__(self, *args, **kwargs):
        """
        Обязательно! Вызов краулера
        :return: object class Crawl __call__
        """
