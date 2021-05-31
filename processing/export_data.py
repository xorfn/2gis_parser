import json
import csv
from models.sqlite import SqliteDb


class ExportData(SqliteDb):
    def __init__(self):
        self.result = {}
        super().__init__()

    def _export_to(self,link, h1, phones, emails, type_format="csv", config_table=None):
        if type_format == 'json':
            self.export_json(h1, phones, emails)

        elif type_format == 'csv':
            self.export_csv(h1, phones, emails)

        elif type_format == "db":
            if all(config_table):
                self.export_db(link, h1, phones, emails, config_table)
            else:
                raise Exception("Нет данных о создаваемой таблице")
        else:
            raise Exception(f'Несуществует экспорта для {type_format}. Выберите формат экспорта csv или json')

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

    def export_db(self, link, h1, phones, emails, config_table):
        table, column = config_table

        data_db = {

            'h1': h1,
            'phones': ', '.join([phone.get_attribute('href').split(":")[1] for phone in phones]),
            'emails': ', '.join([email.get_attribute('href').split(":")[1] for email in emails if
                       "@" in email.get_attribute('href').split(":")[1]])
        }

        write_data = f"""update {table} set {column[0]} = '{data_db['h1']}', {column[1]} = '{data_db['phones']}', 
                        {column[2]}='{data_db['emails']}' where url = '{link}' """
        self.execute_db(write_data, commit_db=True)
