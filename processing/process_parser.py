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


class Config:

    _options = webdriver.FirefoxOptions()
    _user_agent = None
    _path_dir = None

    def __init__(self):
        self._profile = webdriver.FirefoxProfile()
        self.queue = queue.Queue()
        self._driver = self.web_driver()

    @property
    def path_dir(self):
        return self._path_dir

    @path_dir.setter
    def path_dir(self, value):
        if self._path_dir is None:
            self._path_dir = value

    def web_driver(self):
        if os.path.exists(self._path_dir):
            self._profile.set_preference("general.useragent.override", f'{self._user_agent}')
            return webdriver.Firefox(self._profile, executable_path=self._path_dir, options=self._options)
        else:
            raise FileExistsError(f"Не найден web_driver на пути {self._path_dir}")


class ParserGis(Config):
    def __init__(self):
        self._url = None
        self._close_popup = None
        self._click_next_page = None
        self._select_obj_href = None
        Config.__init__(self)

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

    def close_popup_cookies(self):
        try:
            self._driver.find_element_by_xpath(self._close_popup).click()
        except NoSuchElementException:
            print(f"Элемента нет")

    def execute_parser(self):
        try:
            self._driver.get(self._url)
            print(f"Запущено: {self._url}")
        except Exception as e:
            print(f"Что-то пошло не так: {e}")

        self.close_popup_cookies()

    def __parser(self):
        time.sleep(random.randint(2, 6))
        href = self._driver.find_elements_by_css_selector(self._select_obj_href)

        for elem in href:
            self.queue.put(elem.get_attribute('href').split("?")[0])

    def run_parser(self, next_page=True):
        self.__parser()
        if next_page:
            self.__next_pages()
        else:
            print(f"Собрано ссылок {self.queue.qsize()}")
            print(list(self.queue.queue))
            return self.queue

    def __next_pages(self):
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


class Crawl(Config, ExportData):
    def __init__(self, links, export=None, config_table=None):
        self._links = links
        self.export = export
        self.config_table = config_table
        self._click_more_phone = None
        self._fetch_h1 = None
        self._fetch_phones = None
        self._fetch_emails = None
        Config.__init__(self)
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
        name = self._driver.find_element_by_xpath(h1).text
        phones = self._driver.find_elements_by_css_selector(phone)
        emails = self._driver.find_elements_by_css_selector(email)
        return name, phones, emails

    def execute_crawler(self, links):
        while True:
            item = links.get()
            self._driver.get(item)

            #time.sleep(random.randint(2, 3))

            try:
                click_more_phone = self._driver.find_element_by_xpath(self._click_more_phone)
                self._driver.execute_script("arguments[0].click();", click_more_phone)
            except NoSuchElementException:
                pass

            h1, phones, emails = self.collect_data(self._fetch_h1, self._fetch_phones, self._fetch_emails)
            try:
                self._export_to(h1, phones, emails, type_format=self.export, config_table=self.config_table)
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

    def __call__(self):
        thread = [
            threading.Thread(target=self.execute_crawler, args=(self._links,), daemon=True)
        ]
        for t in thread:
            t.start()
        self._links.join()

        print("Все объекты обработаны")


class GenSpider(ABC):
    def __init__(self):
        Config._path_dir = self.driver()
        Config._options.headless = self.headless()
        Config._user_agent = self.user_agent()
        self.parser = ParserGis()
        self.parser.settings = self.config_window_parser()
        self.parser.start_url = self.start_url()
        self.parser.run_parser()
        self.crawler = self.__crawler()
        self.fetch_elements = self.fetch_element()

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

    @abstractmethod
    def user_agent(self):
        """
        Установка юзер-агента
        :return: str
        """

    @abstractmethod
    def start_url(self):
        """
        Стартовый URL
        :return: str
        """

    @abstractmethod
    def config_window_parser(self):
        """
        Конфигуратор окна. Закрытие всяких попапов, хождение по пагинации, выбор селекта детального объекта
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

    def __config_table(self):
        if self.export_data() == "db":
            return self.table_db(), self.column_db()

    def __crawler(self):
        return Crawl(self.parser.queue, export=self.export_data(), config_table=self.__config_table())

    @abstractmethod
    def fetch_element(self):
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
