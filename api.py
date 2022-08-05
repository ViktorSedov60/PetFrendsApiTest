import pytest
import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder
from settigs import *




class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"


    def get_api_key(self, email: str, password: str):
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
              с уникальным ключем  пользователя с указанным email и паролем"""

        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url+'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()

        except:
            result = res.text

        return status, result

    # @pytest.fixture()
    # # Получение ключа auth_key
    # def get_api_keys(self):
    #     headers = {'email': valid_email, 'password': valid_password}
    #     res = requests.get("https://petfriends.skillfactory.ru/api/key", headers=headers)
    #     optional = res.request.headers
    #     assert optional.get('email') == valid_email
    #     assert optional.get('password') == valid_password
    #     status = res.status_code
    #     try:
    #         result = res.json()
    #     except json.decoder.JSONDecodeError:
    #         result = res.text
    #     return status, result





    def get_list_of_pets(self, auth_key, filter):
        """Метод отправляет запрос на сервер о данных всех питомцув  или по фильтру и возвращает
                       статус запроса и result в формате JSON с  данными всех  питомцев или по фильтру.  """

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)
        content = res.headers
        optional = res.request.headers
        status = res.status_code
        result = ""
        try:
            result = res.json()

        except:
            result = res.text

        return status, result, content, optional

    def add_new_pet(self, auth_key, name, animal_type, age, pet_photo):
        """Метод отправляет (постит) на сервер данные о добавляемом питомце и возвращает статус
           #     запроса на сервер и результат в формате JSON с данными добавленного питомца"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpg')
            })

        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        print(res)
        status = res.status_code
        result = ""
        try:
            result = res.json()

        except:
            result = res.text

        return status, result





    def update_pet_info(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: int) -> json:
        """Метод отправляет запрос на сервер о обновлении данных питомуа по указанному ID и возвращает
        статус запроса и result в формате JSON с обновлённыи данными питомца. При отсутствии питомца  тест выполнен,
        но указывает: There is no my pets """

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result



    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает статус запроса и
        результат в формате JSON с текстом уведомления о успешном удалении. При отсутствии питомца тест выполнен,
        но указывает: There is no my pets  """

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result



    def add_new_pet_simple(self, auth_key, name, animal_type, age):
        """Метод отправляет (постит) на сервер данные о добавляемом питомце без фото и возвращает статус
           #     запроса на сервер и результат в формате JSON с данными добавленного питомца"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result



    def delete_all_pet(self, auth_key: json, pet_id: str) -> json:


        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)

        status = res.status_code
        result = ""
        try:
            result = res.json()
            print(result)
        except:
            result = res.text
            print(result)
        return status, result