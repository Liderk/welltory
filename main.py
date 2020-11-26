from jsonschema import validate, Draft7Validator
import json
import os


class ValidateJson:
    def __init__(self, file, schemas):
        self.file = file
        self.schemas = schemas
        self.messages = []

    def _write_log_file(self):
        with open('errors.log', 'a') as logfile:
            logfile.write(f'в файле {self.file}' + '\n')
            for message in self.messages:
                logfile.write(message + '\n')
            logfile.write('_______________' + '\n')

    def load_json(self):
        with open(f'event/{self.file}', 'r', encoding='utf-8') as read_j:
            data = json.load(read_j)
        return data

    def _get_schema(self, json_data):
        schema_name = json_data.get('event', None)
        if not schema_name:
            return False, f'В файле {self.file}  не указанно название схемы'
        if f'{schema_name}.schema' not in self.schemas:
            return False, 'Нет такой схемы'
        with open(f'schema/{schema_name}.schema', "r",
                  encoding="utf-8") as schema:
            schema_obj = json.load(schema)
            return True, schema_obj

    def _is_json_valid(self, json_data):
        if not json_data:
            return False, f' Файл {self.file} не содержит json'
        data = json_data.get('data', None)
        if not data:
            return False, f' Нет данных в файле {self.file}'
        if not isinstance(data, dict):
            return False, f'{self.file} это не json'
        return True, data

    def validate(self):
        json_data = self.load_json()
        json_is_valid, data = self._is_json_valid(json_data)

        if json_is_valid:
            schema_is_valid, json_schema = self._get_schema(json_data)

            if schema_is_valid:
                instance = data
                validator = Draft7Validator(json_schema)
                if validator.is_valid(instance):
                    self.messages.append('все хорошо')
                else:
                    errors = validator.iter_errors(instance)
                    for error in errors:
                        self.messages.append(error.message)

            else:
                self.messages.append(json_schema)
        else:
            self.messages.append(data)

        self._write_log_file()


def main():
    json_files = os.listdir('event')
    schemas = os.listdir('schema')
    for file in json_files:
        t = ValidateJson(file, schemas)
        t.validate()
    # schema_dir = os.path.abspath('schema')
    # event_dir = os.path.abspath('event')
    # schemas = os.listdir(schema_dir)
    # events = os.listdir(event_dir)
    #
    # for event in events:
    #     event_file_name = os.path.join(event_dir, event)
    #     t = ValidateJson(event_file_name, schemas)
    #     t.validate()


if __name__ == '__main__':
    main()
