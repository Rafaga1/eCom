import unittest
import requests


class Testing(unittest.TestCase):

    def test_valid_params(self):
        url = 'http://0.0.0.0:8000/get_form?'
        test_params = {
            'OrderMode': 'order_date=01.04.2019&courier_phone=+79874436278&supplier_name_text=str&order_list_text=str',
            'FamilyModel': 'birthday_data=2009.05.21&dad_phone=+79862435427&dad_email=petrov_s@yandex.ru&description_text=Тут какой то текст',
            'CoworkerContactModel': "phone=+99263458748&email=djfhtn@gmail.com&name_text=Тут тоже текст 23у"
        }

        for name, data in test_params.items():
            result = requests.post(f'{url}{data}')
            self.assertEqual(result.status_code, 200)
            self.assertEqual(result.text.replace('"', ''), name)

    def test_invalid_params(self):
        url = 'http://0.0.0.0:8000/get_form?'
        test_params = {
            'OrderMode': 'order_date=01.40.2019&courier_phone=+79874436278&supplier_name_text=str&order_list_text=str',
            'FamilyModel': 'birthday_data=2009.05.21&dad_phone=79862435427&dad_email=petrov_s@yandex.ru&description_text=Тут какой то текст',
            'CoworkerContactModel': "phone=+99263458748&email=djfhtn@gmail.co.m&name_text=Тут тоже текст 23у"
        }

        # result = requests.post(f'{url}{test_params["OrderMode"]}')
        # self.assertEqual(result.status_code, 400)
        # self.assertNotEqual(result.text.replace('"', ''), 'OrderMode')
        # print(result)
        for name, data in test_params.items():
            result = requests.post(f'{url}{data}')
            self.assertEqual(result.status_code, 400)
            self.assertNotEqual(result.text.replace('"', ''), name)


# http://127.0.0.1:8000/get_form?order_date=01.04.2019&courier_phone=+79874436278&supplier_name_text=str&order_list_text=str