import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder




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

    def get_list_of_pets(self, auth_key, filter):
        """Метод отправляет запрос на сервер о данных всех питомцув  или по фильтру и возвращает
                       статус запроса и result в формате JSON с  данными всех  питомцев или по фильтру.  """

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()

        except:
            result = res.text

        return status, result

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



    def get_list_my_pets(self, auth_key: json) -> json:

        """Метод отправляет запрос на сервер о данных моего питомца по указанному ID и возвращает
                статус запроса и result в формате JSON с  данными питомца. При отсутствии питомца  тест выполнен,
                но указывает: There is no my pets """

        headers = {'auth_key': auth_key['key']}

        res = requests.get(self.base_url+'my_pets', headers=headers)

        status = res.status_code
        result = ""
        try:
            result = res.json()

        except json.decoder.JSONDecodeError:
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



    def add_pet_not_photo(self, auth_key, name, animal_type, age):
        """Метод отправляет (постит) на сервер данные о добавляемом питомце без фото и возвращает статус
           #     запроса на сервер и результат в формате JSON с данными добавленного питомца"""

        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        headers = {'auth_key': auth_key['key']}

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        print(res)
        status = res.status_code
        result = ""
        try:
            result = res.json()

        except:
            result = res.text

        return status, result
