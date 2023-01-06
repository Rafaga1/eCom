import re
import datetime
from email_validator import validate_email, EmailSyntaxError, EmailUndeliverableError
from tinydb import TinyDB

db = TinyDB('db.json')
form = db.table('FORMS')
fields = db.table('fields')
FORMS = form.all()[0]
FIELDS = fields.all()[0]


async def date_validator(date_str: str) -> bool:
    """
    Валидация даты. Принимает строку
    Y.m.d пример 10.03.2003
    Y.m.d пример 2003.10.03
    Если дата валидна, возвращает True, в противном случае False
    :param date_str: str
    :return bool
    """
    try:
        datetime.datetime.strptime(date_str, "%d.%m.%Y").date().strftime("%d.%m.%Y")
        return True
    except ValueError:
        pass

    try:
        datetime.datetime.strptime(date_str, "%Y.%m.%d").date().strftime("%d.%m.%Y")
        return True
    except ValueError:
        raise TypeError


async def phone_validator(phone_str: str) -> bool:
    """
    Валидация телефона. Номер должен начинаться со знака + далее 10 цифр.
    Принимает строку. Образец: +7987334652
    :param phone_str: str
    :return: bool
    """
    regex = r"^(\+)[1-9][0-9\-\(\)\.]{10}$"
    if re.search(regex, phone_str):
        return True
    else:
        raise TypeError


async def email_validator(email_str: str) -> bool:
    """
    Валидатор email. Принимает строку. Если email валиден, возвращает True, иначе False.
    :param email_str: str
    :return: bool
    """
    try:
        email_str = email_str.replace('%40', '@')
        validate_email(email_str)
        return True
    except EmailSyntaxError:
        raise TypeError
    except EmailUndeliverableError:
        raise TypeError


async def check_incoming_data(found_form: str, incoming_dict: dict) -> bool | str:
    """
    Проверка валидности пришедьших данных
    :param found_form: str
    :param incoming_dict: dict
    :return: str
    """
    exist_form = FORMS.get(found_form)

    try:
        for name, field_type in exist_form.items():
            field_data = incoming_dict.get(name)
            if field_type == 'date':
                await date_validator(field_data)
            elif field_type == 'phone':
                await phone_validator(field_data)
            elif field_type == 'email':
                await email_validator(field_data)
    except TypeError:
        return False
    return found_form

async def incoming_parser(icoming: str) -> dict:
    """
    Создание словаря из пришедьших данных.
    :param icoming: str
    :return: dict
    """
    try:
        incoming_dict = {}
        for kv_pair in icoming.split('&'):
            k, v = kv_pair.split('=')
            incoming_dict[k] = v
    except Exception:
        return False
    return incoming_dict



async def field_comparison(form1: dict, form2: dict) -> bool:
    """
    Проверка вхождения полей из имеющейся формы в списке полей пришедьших данных.
    :param form1: dict
    :param form2: dict
    :return: bool
    """
    a = list(form2.keys())
    b = list(form1.keys())[1:]
    if all(field in list(form2.keys()) for field in list(form1.keys())[1:]):
        return True
    else:
        return False


async def find_form(incoming_form: dict) -> str | bool:
    """
    Поис подходящей формы исходя из пришедьших полей.
    Если форма найдена, аозвращает имя найденной формы, иначе False
    :param incoming_form: dict
    :return: str | bool
    """
    for name_form, form in FORMS.items():
        comparison_result = await field_comparison(form, incoming_form)
        if comparison_result:
            return name_form
    return False

async def return_right_type(incoming_dict: dict) -> dict:
    """
    Ключам пришедьших полей выставляет ожидаемый тип данных.
    Если такого поля нет, значением становится: Такого поля нет.
    :param incoming_dict: dict
    :return: dict
    """
    for field, _ in incoming_dict.items():
        incoming_dict[field] = FIELDS.get(field, 'Такого поля нет.')
    return incoming_dict
