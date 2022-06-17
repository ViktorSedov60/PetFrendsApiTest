from api import  PetFriends
from settigs import *
import pytest
import os


class TestPetFriends:
    def setup(self):
        self.pf = PetFriends()

    def test_get_api_key(self, email=valid_email, password=valid_password):
        status, result = self.pf.get_api_key(email, password)
        assert status == 200
        assert 'key' in result

    def test_get_not_api_key(self, email=invalid_email, password=invalid_password):
        # тест на некорректные логин с паролем
        status, result = self.pf.get_api_key(email, password)
        assert status == 403


    def tests_get_all_pets(self, filter=''):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        status, result = self.pf.get_list_of_pets(auth_key, filter)
        assert status == 200
        assert len(result['pets']) > 0

    def tests_get_my_filter_pets(self, filter='my_pets'):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        try:
            status, result = self.pf.get_list_of_pets(auth_key, filter)
            assert status == 200
            assert len(result['pets']) > 0
        except:
            print(' status = ', status)
            print('There is no my pets')




    def tests_add_new_pet(self, name='pig', animal_type='swan', age='2', pet_photo='..\images\swan.jpg'):
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        status, result = self.pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        assert status == 200
        assert result['name'] == name

    def tests_get_my_pet(self):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        _, myPets = self.pf.get_list_of_pets(auth_key, "my_pets")
        status, result = self.pf.get_list_my_pets(auth_key)
        if len(myPets['pets']) > 0:
            assert status == 200
            assert 'name' in result
        else:
            print(' status = ', status)
            print("There is no my pets")


    def tests_put_my_pet(self, name='svin', animal_type='pig', age=5):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        _, myPets = self.pf.get_list_of_pets(auth_key, "my_pets")


        if len(myPets['pets']) > 0:
            status, result = self.pf.update_pet_info(auth_key, myPets['pets'][0]['id'], name, animal_type, age)

            assert status == 200
            assert result['name'] == name

        else:
            print("There is no my pets")


    def tests_add_my_pet(self, name='svin', animal_type='pig', age=5):
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        status, result = self.pf.add_pet_not_photo(auth_key, name, animal_type, age)

        assert status == 200
        assert result['name'] == name

    def tests_add_my_negat_pet(self, name='svin', animal_type='pig', age=5):
        # добавляем пета с использованием ключа, забитого в settigs.py.
        # В случае неправильного ключа тест выполняется с указанием status_code и incorrect auth_key
        try:
            status, result = self.pf.add_pet_not_photo(auth_key, name, animal_type, age)
            assert status == 200
            assert result['name'] == name
        except:
            print('incorrect auth_key')


    def test_delet_my_one_pet(self):
        # Убираем одного пета (по индексу "0")

        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        status, myPets = self.pf.get_list_of_pets(auth_key, "my_pets")

        if len(myPets['pets']) > 0:
            pet_id = myPets['pets'][0]['id']
            status, _ = self.pf.delete_pet(auth_key, pet_id)

            assert status == 200
            assert pet_id not in myPets.values()

        else:
            print(' status = ', status)
            print("There is no my pets")


    def test_delet_my_all_pets(self):
        # Убираем всех своих петов
        _, auth_key = self.pf.get_api_key(valid_email, valid_password)
        status, myPets = self.pf.get_list_of_pets(auth_key, "my_pets")


        for i in range(len(myPets['pets'])):
            pet_id = myPets['pets'][i]['id']
            status, _ = self.pf.delete_pet(auth_key, pet_id)

        try:
            assert status == 200
            assert pet_id not in myPets.values()
        except:
            print(' status = ', status)
            print("There is no my pets")






