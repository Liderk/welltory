import json
import os

from jsonschema import Draft7Validator


class ValidateJson:
    """Проверяет json файлы на ошибки, в соотвестви с их schema. После чего
    формирует списки ошибок и записывает их в errors.log с подробным описанием
    ошибки, где она находится, и как её исправить"""
    SCHEMAS = os.listdir('schema')

    def __init__(self, schemas=None):
        self.schemas = []
        if schemas:
            self.schemas += schemas
        else:
            self.schemas += ValidateJson.SCHEMAS
        self.errors = []
        self.message = []

    def _errors(self):
        """Формирует список ошибок при валидации json файла.
        Список формируется в зависимости от типа ошибки."""
        if not self.errors:
            return

        for error in self.errors:
            if isinstance(error, str):
                self.message.append(error)
                self.message.append('________________')
            else:
                error_value = error.message.split("'")[1]
                instanse_error_path = error.absolute_path.copy()

                if error.validator == 'type':
                    self.message.append(f'Type error: {error.message}')
                    self.message.append(f'Type must be: '
                                        f'"{error.validator_value}"')

                if error.validator == 'required':
                    self.message.append(f"Key not found: '{error_value}'")
                    self.message.append(f'Must be all key: '
                                        f'{error.validator_value}')

                if len(instanse_error_path) > 1:
                    self.message.append(
                        f'Instanse key path: '
                        f'file["{error.absolute_path.popleft()}"]'
                        f'[{error.absolute_path.popleft()}]')
                elif len(instanse_error_path) == 1:
                    self.message.append(
                        f'Instanse key path: '
                        f'file["{error.absolute_path.popleft()}"]')
                else:
                    self.message.append(
                        f'Instanse key path: file[]')

                if len(instanse_error_path) == 0:
                    self.message.append(
                        f'Current value: missed ')
                else:
                    self.message.append(
                        f'Current value: "{error.instance}"')
                self.message.append('________________')

        self._write_log_file()

    def _write_log_file(self):
        """Запись ошибок в лог файл"""
        with open('errors.log', 'a') as logfile:
            for message in self.message:
                logfile.write(message + '\n')

    def _load_json(self, file):
        """Считывает json-файл."""
        with open(f'event/{file}', 'r', encoding='utf-8') as read_j:
            data = json.load(read_j)
        return data

    def _check_error_in_json_file(self, json_data):
        """Проверяет ошибки в json файле"""
        if not json_data:
            return 'The file does not contain JSON'
        data = json_data.get('data', None)
        if not data:
            return 'There is no data in the file'
        if not isinstance(data, dict):
            'File is not JSON-file'
        return None

    def _check_schema_errors(self, json_data):
        """Ищет соотвествие schema и json фала.
        Проверяет на наличие возможных ошибок"""
        schema_name = json_data.get('event', None)
        if not schema_name:
            return 'Key "event" was not found in the json file. '
        if f'{schema_name}.schema' not in self.schemas:
            return 'The schema name contains an error in key "event",' \
                   ' or there is no such schema.' \
                   ' Check the "event" key in the json file.'
        return None

    def _get_schema(self, schema_name):
        """Получает структуру schema для дальнейшей валидации json файла """
        with open(f'schema/{schema_name}.schema', "r",
                  encoding="utf-8") as schema:
            schema_obj = json.load(schema)
            return schema_obj

    def validate(self, file):
        """Проводит валидацию json файлов в соотвествии с их schema"""
        self.message.append(f'Error in file: {file}')
        json_data = self._load_json(file)
        json_errors = self._check_error_in_json_file(json_data)
        if not json_errors:
            schema_errors = self._check_schema_errors(json_data)
            if not schema_errors:
                instance = json_data['data']
                schema = self._get_schema(json_data['event'])
                validator = Draft7Validator(schema)
                for error in sorted(validator.iter_errors(instance),
                                    key=lambda e: e.path):
                    self.errors.append(error)
            else:
                self.errors.append(schema_errors)
        else:
            self.errors.append(json_errors)
        return self._errors()


def main():
    json_files = os.listdir('event')
    schemas = os.listdir('schema')
    for file in json_files:
        t = ValidateJson(schemas)
        t.validate(file)


if __name__ == '__main__':
    main()
