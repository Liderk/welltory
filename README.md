# welltory test task

Проверяет json файлы на ошибки, в соотвестви с их schema. После чего
формирует списки ошибок и записывает их в errors.log с подробным описанием
ошибки, где она находится, и как её исправить.


json файлы лежат в папке 'event' схемы в папке 'schema'  в директории скрипта.

## Запуск скрипта
Для запуска скрипта необходимо установить зависимости

```pip install -r requirements.txt```


Далее запустить скрипт

```python3 json_validator.py```

Результат работы посмотреть в файле *errors.log*

