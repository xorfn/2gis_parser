import json
import csv
from models.sqlite import SqliteDb


class ExportData(SqliteDb):
    def __init__(self):
        super(SqliteDb, self).__init__()
        self.result = {}

    def _export_to(self,h1, phones, emails, type_format="csv", config_table=None):
        if type_format == 'json':
            self.export_json(h1, phones, emails)

        elif type_format == 'csv':
            self.export_csv(h1, phones, emails)

        elif type_format == "db":
            if all(config_table):
                self.export_db(h1, phones, emails, config_table)
            else:
                raise Exception("Нет данных о создаваемой таблице")
        else:
            raise ValueError(f'Несуществует экспорта для {type_format}. Выберите формат экспорта csv или json')

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

    def export_db(self, h1, phones, emails, config_table):
        table, column = config_table

        check_db = f"""select * from {table}"""
        create_table = f"""CREATE TABLE {table} (PK INTEGER NOT NULL, {column[0]} TEXT, {column[1]} TEXT, {column[2]} TEXT, PRIMARY KEY (PK))"""

        data_db = {

            'h1': h1,
            'phones': [phone.get_attribute('href').split(":")[1] for phone in phones],
            'emails': [email.get_attribute('href').split(":")[1] for email in emails if
                       "@" in email.get_attribute('href').split(":")[1]]
        }

        data = data_db['h1'], ', '.join(data_db['phones']), ', '.join(data_db['emails'])

        try:
            self.execute_db(check_db)
        except Exception as e:
            if "no such table" in e.args[0]:
                self.execute_db(create_table.format(table=table, *column), commit_db=True)

            write_data = f"""insert into {table} ({column[0]}, {column[1]}, {column[2]}) values (?, ?, ?)"""
            self.execute_db(write_data, (*data,), commit_db=True)

        else:
            write_data = f"""insert into {table} ({column[0]}, {column[1]}, {column[2]}) values (?, ?, ?)"""
            self.execute_db(write_data, (*data,), commit_db=True)