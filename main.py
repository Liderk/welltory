from jsonschema import Draft7Validator
import json
import os


class ValidateJson:
    def __init__(self, schemas):
        self.schemas = schemas
        self.errors = []
        self.message = []

    def _errors(self):
        if not self.errors:
            return

        for error in self.errors:
            if isinstance(error, str):
                self.message.append(error)
                self.message.append('________________')
            else:

                self.message.append(error.message)
                self.message.append(f'Instanse field path {error.absolute_path}')
                if len(error.absolute_path) != 0:
                    self.message.append(f'Current value "{error.instance}"')
                self.message.append(error.validator)
                self.message.append('________________')

        self._write_log_file()


    def _write_log_file(self):
        with open('errors.log', 'a') as logfile:
            for message in self.message:
                logfile.write(message + '\n')
            # logfile.write('_______________' + '\n')



    def _load_json(self, file):
        with open(f'event/{file}', 'r', encoding='utf-8') as read_j:
            data = json.load(read_j)
        return data

    def _check_error_in_json_file(self, json_data):
        if not json_data:
            return 'Файл не содержит json'
        data = json_data.get('data', None)
        if not data:
            return 'Нет данных в файле'
        if not isinstance(data, dict):
            'Это не json'
        return None

    def _check_schema_errors(self, json_data):
        schema_name = json_data.get('event', None)
        if not schema_name:
            return 'В файле не указанно название схемы'
        if f'{schema_name}.schema' not in self.schemas:
            return 'Ошибка названии схемы в поле "event", ' \
                   'либо такой схемы не существует'
        return None

    def _get_schema(self, schema_name):
        with open(f'schema/{schema_name}.schema', "r",
                  encoding="utf-8") as schema:
            schema_obj = json.load(schema)
            return schema_obj

    def validate(self, file):
        self.message.append(f'Error in file: {file}')
        json_data = self._load_json(file)
        json_errors = self._check_error_in_json_file(json_data)
        if not json_errors:
            schema_errors = self._check_schema_errors(json_data)
            if not schema_errors:
                instance = json_data['data']
                schema = self._get_schema(json_data['event'])
                validator = Draft7Validator(schema)
                for error in sorted(validator.iter_errors(instance), key=lambda e: e.path):
                    self.errors.append(error)
            else:
                self.errors.append(schema_errors)
        else:
            self.errors.append(json_errors)
        return self._errors()


def main():
    json_files = os.listdir('event')
    # file = '297e4dc6-07d1-420d-a5ae-e4aff3aedc19.json'
    schemas = os.listdir('schema')
    # t = ValidateJson(schemas)
    # t.validate(file)
    for file in json_files:
        t = ValidateJson(schemas)
        t.validate(file)


if __name__ == '__main__':
    main()
