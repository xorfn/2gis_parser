from parser_2gis import ParserGis, Crawl, ConfigSpider


def run():
    # Включкение безголового режима
    ConfigSpider.options.headless = True
    # Ссылка на web_driver
    ConfigSpider.pathD = r'C:\Users\Xorex\PycharmProjects\2gis_parser\driver\geckodriver.exe'
    # Установка юзер агента
    ConfigSpider.options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ("
                                      "KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36")
    # Стартовый URL
    url = "https://2gis.ru/krasnodar/search/%D0%9F%D0%B0%D1%80%D0%B8%D0%BA%D0%BC%D0%B0%D1%85%D0%B5%D1%80%D1%81%D0%BA" \
          "%D0%B8%D0%B5/rubricId/305/filters/bound%3Bcovid_services_home%3Bgeneral_payment_type_card%3Bhas_site" \
          "%3Bhas_photos"

    # Запуск парсера
    p = ParserGis(url=url)
    p.parser_pages(next_page=True)
    print(p.links)
    result = Crawl(p.links, export='json')

    return result()


if __name__ == "__main__":
    run()
