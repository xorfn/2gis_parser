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

class Conf:
    def __init__(self):
        self._options = webdriver.FirefoxOptions()
        self._profile = webdriver.FirefoxProfile()
        self._path_dir = r'C:\Users\Xorex\PycharmProjects\2gis_parser\driver\geckodriver.exe'
        self.user_agent = "User-agent/5.0"
        self._driver = self.web_driver()
        self.queue = queue.Queue()
        self.close_popup = self.close_popup()
        self.click_next_page = self.click_next_page()
        self.select_obj_href = self.select_obj_href()
        self.click_more_phone = self.click_more_phone()

    def web_driver(self):
        if os.path.exists(self._path_dir):
            self._profile.set_preference("general.useragent.override", f'{self.user_agent}')
            return webdriver.Firefox(self._profile, executable_path=self._path_dir, options=self._options)
        else:
            raise FileExistsError("Не найден web_driver.")
    def close_popup(self):
        close_popup = '//*[@id="root"]/div/div/div[3]/footer/div[2]'
        return close_popup

    def click_next_page(self):
        click_next_page = '//*[@id="root"]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/div[2]/div[' \
                          '2]/div[1]/div/div/div[1]/div[3]/div[2]/div[2]'
        return click_next_page

    def select_obj_href(self):
        select_obj_href = "div._1h3cgic > a._pbcct4"
        return select_obj_href

    def click_more_phone(self):
        click_more_phone = '//*[@class="_b0ke8"]/a'
        return click_more_phone

class ParserGis(Conf):
    def __init__(self):
        super().__init__()
        self._url = ''

    @property
    def start_url(self):
        return self._url

    @start_url.setter
    def start_url(self, value):
        if self._url == '':
            self._url = value
            self.execute_parser()

    @property
    def headless(self):
        return self._options

    @headless.setter
    def headless(self, v):
        if self._options:
            self._options.headless = v


    def close_popup_cookies(self):
        try:
            self._driver.find_element_by_xpath(self.close_popup).click()
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
        href = self._driver.find_elements_by_css_selector(self.select_obj_href)

        for elem in href:
            self.queue.put(elem.get_attribute('href').split("?")[0])

    def parser_pages(self, next_page=None):
        self.__parser()
        if next_page or next_page is None:
            self.__next_pages()
        else:
            print(f"Собрано ссылок {self.queue.qsize()}")
            return self.queue

    def __next_pages(self):
        if "2gis" in self._driver.current_url:
            try:
                self._driver.find_element_by_xpath(self.click_next_page).click()
                self.parser_pages()
            except NoSuchElementException:
                self.parser_pages(next_page=False)
                self._driver.close()
                self._driver.quit()

    def queue_exp(self):
        return self.queue.qsize()


class Crawl(Conf):
    def __init__(self, links, export=None):
        super().__init__()
        self.result = {}
        self.__links = links
        self.export = export
        self.h1 = '//h1'
        self.phones = "div._49kxlr > div._b0ke8 > a._1nped2zk"
        self.emails = "div._49kxlr > div > a._1nped2zk"

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
        with open("2gis.json", "w", encoding="utf-8") as file:
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
        with open("2gis.csv", "a") as file:
            writer = csv.writer(file, delimiter=";", lineterminator="\r")
            writer.writerow((org_to_csv['name'], org_to_csv['phones'], ', '.join(org_to_csv['emails'])))

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

            h1, phones, emails = self.collect_data(self.h1, self.phones, self.emails)

            if self.export == 'json':
                self.export_json(h1, phones, emails)

            elif self.export == 'csv':
                self.export_csv(h1, phones, emails)
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
