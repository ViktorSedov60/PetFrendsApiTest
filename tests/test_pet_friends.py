from api import  PetFriends
from settigs import *
from conftest import *
import pytest
import os
import json
import requests
import inspect  # используем метод для возвращения имени функции


pf = PetFriends()

def generate_string(n):
   return "x" * n

def russian_chars():
   return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


def chinese_chars():
   return '的一是不了人我在有他这为之大来以个中上们'


def special_chars():
   return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'


@pytest.fixture(autouse=True)
def ket_api_key():
   #""" Проверяем, что запрос api-ключа возвращает статус 200 и в результате содержится слово key"""

   # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
   status, pytest.key = pf.get_api_key(valid_email, valid_password)

   # Сверяем полученные данные с нашими ожиданиями
   assert status == 200
   assert 'key' in pytest.key

   yield


@pytest.mark.parametrize("filter",
                        [
                            generate_string(255)
                            , generate_string(1001)
                            , russian_chars()
                            , russian_chars().upper()
                            , chinese_chars()
                            , special_chars()
                            , 123
                        ],
                        ids =
                        [
                            '255 symbols'
                            , 'more than 1000 symbols'
                            , 'russian'
                            , 'RUSSIAN'
                            , 'chinese'
                            , 'specials'
                            , 'digit'
                        ])
# negative test
def test_get_all_pets_with_negative_filter(filter):
   pytest.status, result, _, _ = pf.get_list_of_pets(pytest.key, filter)

   # Проверяем статус ответа
   assert pytest.status == 400


@pytest.mark.parametrize("filter",
                        ['', 'my_pets'],
                        ids=['empty string', 'only my pets'])

# pozitive test
def test_get_all_pets_with_valid_key(filter):
   pytest.status, result, _, _ = pf.get_list_of_pets(pytest.key, filter)

   # Проверяем статус ответа
   assert pytest.status == 200
   assert len(result['pets']) > 0



# @pytest.fixture(autouse=True)
# def ket_api_key():
#     status, pytest.key = pf.get_api_key(valid_email, valid_password)
#     assert status == 200
#     assert 'key' in pytest.key
#
#     yield
#
#     assert pytest.status == 200

@pytest.mark.parametrize("filter", ['', 'my_pets'], ids= ['empty string', 'only my pets'])
def test_get_all_pets_with_valid_key(filter):
    pytest.status, result, _, _ = pf.get_list_of_pets(pytest.key, filter)

    assert len(result['pets']) > 0




@pytest.mark.parametrize("name", ['', generate_string(255), russian_chars(), '123'],
                         ids=['empty', '255 symbols', 'russian', 'digit'])
@pytest.mark.parametrize("animal_type", ['', generate_string(255), russian_chars(), '123'],
                         ids=['empty', '255 symbols', 'russian', 'digit'])
@pytest.mark.parametrize("age", ['', '-1', '0', '1', '100', '1.5', chinese_chars()],
                         ids=['empty', 'negative', 'zero', 'min', 'greater than max', 'float', 'chinese'])


def test_add_new_pet_simple(name, animal_type, age):
    """Проверяем, что можно добавить питомца с различными данными"""
    # Добавляем питомца
    pytest.status, result = pf.add_new_pet_simple(pytest.key, name, animal_type, age)
    assert pytest.status == 200
    assert result['name'] == name
    assert result['age'] == age
    assert result['animal_type'] == animal_type







def test_get_api_key(get_api_keys):
    result = get_api_keys
    with open("out_json.json", 'w', encoding='utf8') as my_file:
        my_file.write(f'\n{inspect.currentframe().f_code.co_name}:\n')
        json.dump(result, my_file, ensure_ascii=False, indent=4)
    assert 'key' in result

    def test_get_not_api_key(self, email=invalid_email, password=invalid_password):
        # тест на некорректные логин с паролем
        status, result = self.pf.get_api_key(email, password)
        assert status == 403


def tests_get_all_pets(get_api_keys, filter=''):

    status, result, content, optional = pf.get_list_of_pets(get_api_keys, filter)
    print('\nContent:', content)
    print('Optional:', optional)
    assert status == 200
    assert len(result['pets']) > 0

def tests_get_my_filter_pets(get_api_keys, filter='my_pets'):

    try:
        status, result, content, optional  = pf.get_list_of_pets(get_api_keys, filter)
        with open("out_json.json", 'a', encoding='utf8') as my_file:
            my_file.write(f'\n{inspect.currentframe().f_code.co_name}:\n')  # Выводим имя функции, как заголовок ответа
            my_file.write(str(f'\n{status}\n{content}\n{optional}\n'))
            json.dump(result, my_file, ensure_ascii=False, indent=4)
        assert status == 200
        assert len(result['pets']) > 0
    except:
        print(' status = ', status)
        print('There is no my pets')




def tests_add_new_pet(get_api_keys, name='pig', animal_type='swan', age='2', pet_photo='..\images\cor.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    status, result = pf.add_new_pet(get_api_keys, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name



def tests_put_my_pet(get_api_keys, name='сердце', animal_type='человечье', age=60):
    _, myPets, _, _ = pf.get_list_of_pets(get_api_keys, "my_pets")


    if len(myPets['pets']) > 0:
        status, result = pf.update_pet_info(get_api_keys, myPets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name

    else:
        print("There is no my pets")


def tests_add_my_pet(get_api_keys, name='svin', animal_type='suka', age=555):

    status, result = pf.add_new_pet_simple(get_api_keys, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

    def tests_add_my_negat_pet(self, name='svin', animal_type='pig', age=5):
        # добавляем пета с использованием ключа, забитого в settigs.py.
        # В случае неправильного ключа тест выполняется с указанием status_code и incorrect auth_key
        try:
            status, result = self.pf.aadd_new_pet_simple(auth_key, name, animal_type, age)
            assert status == 200
            assert result['name'] == name
        except:
            print('incorrect auth_key')


def test_delet_my_one_pet(get_api_keys):
    # Убираем одного пета (по индексу "0")

    status, resalt, _, _ = pf.get_list_of_pets(get_api_keys, "my_pets")

    if len(resalt['pets']) > 0:
        pet_id = resalt['pets'][0]['id']
        status, _ = pf.delete_pet(get_api_keys, pet_id)

        assert status == 200
        assert pet_id not in resalt.values()

    else:
        print(' status = ', status)
        print("There is no my pets")


def test_delet_my_all_pets(get_api_keys):
    # Убираем всех своих петов
    status, myPets, _, _ = pf.get_list_of_pets(get_api_keys, "my_pets")


    for i in range(len(myPets['pets'])):
        pet_id = myPets['pets'][i]['id']
        status, _ = pf.delete_pet(get_api_keys, pet_id)

    try:
        assert status == 200
        assert pet_id not in myPets.values()
    except:
        print(' status = ', status)
        print("There is no my pets")



@pytest.mark.parametrize("name"
   , [generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(), chinese_chars(),
      special_chars(), '123']
   , ids=['255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("animal_type"
   , [generate_string(255), generate_string(1001), russian_chars(), russian_chars().upper(), chinese_chars(),
      special_chars(), '123']
   , ids=['255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("age", ['1'], ids=['min'])
def test_add_new_pet_simple(name, animal_type, age):
   """Проверяем, что можно добавить питомца с различными данными"""

   # Добавляем питомца
   pytest.status, result = pf.add_new_pet_simple(pytest.key, name, animal_type, age)

   # Сверяем полученный ответ с ожидаемым результатом
   assert pytest.status == 200
   assert result['name'] == name
   assert result['age'] == age
   assert result['animal_type'] == animal_type


@pytest.mark.parametrize("name", [''], ids=['empty'])
@pytest.mark.parametrize("animal_type", [''], ids=['empty'])
@pytest.mark.parametrize("age",
                        ['', '-1', '0', '100', '1.5', '2147483647', '2147483648', special_chars(), russian_chars(),
                         russian_chars().upper(), chinese_chars()]
   , ids=['empty', 'negative', 'zero', 'greater than max', 'float', 'int_max', 'int_max + 1', 'specials',
          'russian', 'RUSSIAN', 'chinese'])
def test_add_new_pet_simple_negative(name, animal_type, age):

   # Добавляем питомца
   pytest.status, result = pf.add_new_pet_simple(pytest.key, name, animal_type, age)

   # Сверяем полученный ответ с ожидаемым результатом
   assert pytest.status == 400






