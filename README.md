
Инструкция.

1) Скопировать с репозитория файлы https://github.com/Rafaga1/eCom
2) запустить команду:
docker build -t foo . && docker run -p 127.0.0.1:8000:8000 -it foo
если порт занят, смените 8000 на другой

Запустится Докер контейнер по адресу http://0.0.0.0:8000
Посмотреть на свагер можно тут: http://0.0.0.0:8000/docs#/


3) Подготовил данные для проверочных POST запросов, отправлять построчно на адрес http://0.0.0.0:8000/get_form? 
Валидные данные:
order_date=01.04.2019&courier_phone=+79874436278&supplier_name_text=str&order_list_text=str
birthday_data=2009.05.21&dad_phone=+79862435427&dad_email=petrov_s@yandex.ru&description_text=Тут какой то текст
phone=+99263458748&email=djfhtn@gmail.com&name_text=Тут тоже текст 23у

Не валидные данные:
order_date=01.40.2019&courier_phone=+79874436278&supplier_name_text=str&order_list_text=str
birthday_data=2009.05.21&dad_phone=79862435427&dad_email=petrov_s@yandex.ru&description_text=Тут какой то текст
phone=+99263458748&email=djfhtn@gmail.co.m&name_text=Тут тоже текст 23у

4) Файл test.py содержит тесты для ендпоинта.

Было бы удобнее валидировать к примеру через Pydantic, но в задании было сказано так. Я решил что это намеренно так написано.
