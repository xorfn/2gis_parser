import csv
import json
import os
import random
import sys
import time
import threading, queue
from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

sys.setrecursionlimit(20000)


# Скачать web_driver
# https://github.com/mozilla/geckodriver/releases

class Config:

    _options = webdriver.FirefoxOptions()
    _user_agent = None
    _path_dir = None

    def __init__(self):
        self._profile = webdriver.FirefoxProfile()
        self._driver = self.web_driver()
        self.queue = queue.Queue()

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
        super().__init__()
        self._url = None
        self._close_popup = None
        self._click_next_page = None
        self._select_obj_href = None

    @property
    def close_popup(self):
        close_popup = '//*[@id="root"]/div/div/div[3]/footer/div[2]'
        return self._close_popup

    @close_popup.setter
    def close_popup(self, value):
        if self._close_popup is None:
            self._close_popup = value

    @property
    def click_next_page(self):
        click_next_page = '//*[@id="root"]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/div[2]/div[' \
                          '2]/div[1]/div/div/div[1]/div[3]/div[2]/div[2]'
        return self._click_next_page

    @click_next_page.setter
    def click_next_page(self, value):
        if self._click_next_page is None:
            self._click_next_page = value

    @property
    def select_obj_href(self):
        select_obj_href = "div._1h3cgic > a._pbcct4"
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


class Crawl(Config):
    def __init__(self, links, export=None):
        super().__init__()
        self.result = {}
        self.__links = links
        self.export = export
        self.click_more_phone = self.click_more_phone()
        self._fetch_h1 = None
        self._fetch_phones = None
        self._fetch_emails = None

    @property
    def fetch_h1(self):
        return self._fetch_h1

    @property
    def fetch_phones(self):
        return self._fetch_phones

    @property
    def fetch_emails(self):
        return self._fetch_emails

    def click_more_phone(self):
        click_more_phone = '//*[@class="_b0ke8"]/a'
        return click_more_phone

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

    def export_json(self, h1, phones, emails):
        org_json = {h1: [{
            "phones": [phone.get_attribute('href').split(":")[1] for phone in phones],
            "emails": [email.get_attribute('href').split(":")[1] for email in emails
                       if "@" in email.get_attribute('href').split(":")[1]],
        }]}

        self.result.update(org_json)
        print([phone.get_attribute('href').split(":")[1] for phone in phones])

        type_json = json.dumps(self.result, ensure_ascii=False)
        with open("company.json", "w", encoding="utf-8") as file:
            file.write(type_json)

    @staticmethod
    def export_csv(h1, phones, emails):
        org_to_csv = {
            'name': h1,
            'phones': [phone.get_attribute('href').split(":")[1] for phone in phones],
            'emails': [email.get_attribute('href').split(":")[1] for email in emails if
                       "@" in email.get_attribute('href').split(":")[1]]
        }

        print([phone.get_attribute('href').split(":")[1] for phone in phones])
        with open("company.csv", "a") as file:
            writer = csv.writer(file, delimiter=";", lineterminator="\r")
            writer.writerow((org_to_csv['name'], org_to_csv['phones'], ', '.join(org_to_csv['emails'])))

    def export_db(self, h1, phones, emails):
        pass

    def execute_crawler(self):
        while True:
            item = self.__links.get()
            self._driver.get(item)

            time.sleep(random.randint(2, 3))

            try:
                click_more_phone = self._driver.find_element_by_xpath(self.click_more_phone)
                self._driver.execute_script("arguments[0].click();", click_more_phone)
            except NoSuchElementException:
                self._driver.get(item + 1)

            h1, phones, emails = self.collect_data(self._fetch_h1, self._fetch_phones, self._fetch_emails)

            if self.export == 'json':
                self.export_json(h1, phones, emails)

            elif self.export == 'csv':
                self.export_csv(h1, phones, emails)
            elif self.export == "db":
                self.export_db(h1, phones, emails)

            else:
                raise ValueError(f'Несуществует экспорта для {self.export}. Выбирите формат экспорта csv или json')

            self.__links.task_done()

            if self.__links.empty():
                print(f"Создан фаил 2gis.{self.export}")
                self._driver.close()
                self._driver.quit()

    def __call__(self, *args, **kwargs):
        threading.Thread(target=self.execute_crawler(), daemon=True).start()
        self.queue.join()


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
        pass

    @abstractmethod
    def headless(self):
        pass

    @abstractmethod
    def user_agent(self):
        pass

    @abstractmethod
    def start_url(self):
        pass

    @abstractmethod
    def config_window_parser(self):
        pass

    @abstractmethod
    def export_data(self):
        pass

    def __crawler(self):
        return Crawl(self.parser.queue, export=self.export_data())

    @abstractmethod
    def fetch_element(self):
        pass

    @abstractmethod
    def crawler(self):
        pass