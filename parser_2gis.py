from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from multiprocessing import Pool

import time
import random
import json, csv
import sys

sys.setrecursionlimit(20000)


# https://chromedriver.storage.googleapis.com/index.html
# https://peter.sh/experiments/chromium-command-line-switches/

class ConfigSpider(object):
    pathD = ''
    options = webdriver.ChromeOptions()

    def __init__(self):
        self.links = []
        self.result = {}
        self.driver = webdriver.Chrome(
            executable_path=self.pathD,
            options=self.options
        )
        self.close_popup = '//*[@id="root"]/div/div/div[3]/footer/div[2]'
        self.click_next_page = '//*[@id="root"]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/div[2]/div[' \
                            '2]/div[1]/div/div/div[1]/div[3]/div[2]/div[2]'


class ParserGis(ConfigSpider):
    def __init__(self, url=None):
        ConfigSpider.__init__(self)
        self.__url = url
        if self.__url:
            self.settings(self.close_popup)

    def settings(self, close_popup):
        try:
            self.driver.get(self.__url)
            print(f"Запущено: {self.__url}")
        except Exception as e:
            print(f"Что-то пошло не так: {e}")

        try:
            self.driver.find_element_by_xpath(close_popup)
            self.driver.find_element_by_xpath(close_popup).click()
            print("Успешно закрыто модальное окно для cookies")
        except NoSuchElementException:
            print(f"Элемента нет")

    def __parser(self):
        time.sleep(random.randint(2, 6))
        href = self.driver.find_elements_by_css_selector("div._1h3cgic > a._pbcct4")

        for elem in href:
            self.links.append(elem.get_attribute('href').split("?")[0])

    def parser(self, next_page=None):
        self.__parser()
        if next_page or next_page is None:
            self.next_pages()
        else:
            print(f"Собрано ссылок {len(self.links)}")
            return self.links

    def next_pages(self):
        if "2gis" in self.driver.current_url:
            try:
                self.driver.find_element_by_xpath(self.click_next_page).click()
                self.parser()
            except NoSuchElementException:
                self.parser(next_page=False)
                self.driver.close()
                self.driver.quit()


class Crawl(ParserGis):
    def __init__(self, links, export=None):
        ParserGis.__init__(self)
        self.__links = links
        self.export = export

    def __call__(self):
        __url = 0
        while __url < len(self.__links):
            self.driver.get(self.__links[__url])
            time.sleep(random.randint(2, 3))
            try:
                try:
                    click_more_phone = self.driver.find_element_by_xpath('//*[@class="_b0ke8"]/a')
                    self.driver.execute_script("arguments[0].click();", click_more_phone)
                except NoSuchElementException:
                    self.driver.get(self.__links[__url + 1])

            except ElementClickInterceptedException:

                click_scroll = self.driver.find_element_by_xpath('//*[@class="_1kmhi0c"]/div').click()
                self.driver.execute_script("arguments[0].click();", click_scroll)

                click_more_phone_e = self.driver.find_element_by_xpath('//*[@class="_b0ke8"]/a')
                self.driver.execute_script("arguments[0].click();", click_more_phone_e)

            name = self.driver.find_element_by_xpath('//h1').text
            phones = self.driver.find_elements_by_css_selector("div._49kxlr > div._b0ke8 > a._1nped2zk")
            emails = self.driver.find_elements_by_css_selector("div._49kxlr > div > a._1nped2zk")

            if self.export == 'json':
                org_json = {name: [{
                    "phones": [phone.get_attribute('href').split(":")[1] for phone in phones],
                    "emails": [email.get_attribute('href').split(":")[1] for email in emails
                               if "@" in email.get_attribute('href').split(":")[1]],
                }]}

                self.result.update(org_json)
                print([phone.get_attribute('href').split(":")[1] for phone in phones])

                type_json = json.dumps(self.result, ensure_ascii=False)
                with open("2gis.json", "w", encoding="utf-8") as file:
                    file.write(type_json)
                __url += 1
            elif self.export == 'csv':
                org_to_csv = {
                    'name': name,
                    'phones': [phone.get_attribute('href').split(":")[1] for phone in phones],
                    'emails': [email.get_attribute('href').split(":")[1] for email in emails if
                               "@" in email.get_attribute('href').split(":")[1]]
                }

                print([phone.get_attribute('href').split(":")[1] for phone in phones])
                with open("2gis", "a") as file:
                    writer = csv.writer(file, delimiter=";", lineterminator="\r")
                    writer.writerow((org_to_csv['name'], org_to_csv['phones'], ', '.join(org_to_csv['emails'])))
                __url += 1
            else:
                raise ValueError(f'Несуществует экспорта для {self.export}. Выбирите формат экспорта csv или json')

        print(f"Создан фаил 2gis.{self.export}")
        self.driver.close()
        self.driver.quit()
