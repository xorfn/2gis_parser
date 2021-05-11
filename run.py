from parser_2gis import ParserGis, Crawl


def parser():
    p = ParserGis()
    p.start_url="https://2gis.ru/krasnodar/search/%D0%9F%D0%B0%D1%80%D0%B8%D0%BA%D0%BC%D0%B0%D1%85%D0%B5%D1%80%D1%81" \
                "%D0%BA%D0%B8%D0%B5/rubricId/305/filters/bound%3Bcovid_services_home%3Bgeneral_payment_type_card" \
                "%3Bhas_site "
    p.parser_pages(next_page=True)
    print(p.links)
    result = Crawl(p.links, export='json')
    return result()


if __name__ == "__main__":
    parser()
