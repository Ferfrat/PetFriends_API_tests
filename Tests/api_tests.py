import os

from api import PetFriends
from settings import valid_email, valid_password, novalid_email, novalid_password

pf = PetFriends()


# 1
def test_get_api_key_for_invalid_email(email=novalid_email, password=valid_password):
    """ Проверяем что запрос к API с неверным email`ом возвращает статус 403"""
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result


# 2
def test_get_api_key_for_invalid_password(email=valid_email, password=novalid_password):
    """ Проверяем что запрос к API с верным email`ом, но неверным паролем возвращает статус 403"""
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result

# 3
def test_get_all_pets_with_novalid_key(filter=''):
    """ Проверяем что запрос всех питомцев c неверным API ключом возвращает статус 403."""
    auth_key = {"key": "oops"}
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 403

# 4
def test_add_new_pet_without_photo_with_valid_data(name='Зараза', animal_type='котярус', age='3'):
    """Проверяем что можно добавить питомца без фото с корректными данными"""

    _,auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

# 5
def test_update_self_pet_info_without_name(name='', animal_type='Котэ', age=5):
    """ Проверяем возможность удалить имя питомца через передачу пустого поля name"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if not my_pets['pets']:
        raise Exception("There is no my pets")
    pet_id = my_pets['pets'][0]['id']

    status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)

    assert status == 200
    assert result['name']

# 6
def test_update_self_pet_info_without_age(name='Бегемотик', animal_type='Котяк', age=''):
    """ Проверяем возможность удалить возраст питомца через передачу пустого поля age"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if not my_pets['pets']:
        raise Exception("There is no my pets")
    pet_id = my_pets['pets'][0]['id']

    status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)

    assert status == 200
    assert result['age']

# 7
def test_add_new_pet_without_photo_without_data(name='', animal_type='', age=''):
    """Проверяем что можно добавить питомца без фото, не внося никакие данные"""

    _,auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

# 8
def test_add_new_pet_without_photo_with_negative_number_of_age(name='Антошка', animal_type='кошандр', age='-3'):
    """Проверяем что можно добавить питомца без фото с отрицательным возрастом"""

    _,auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['age'] == age

# 9
def test_add_new_pet_without_photo_with_strange_animal_type(name='Пухлик', animal_type='@/+?!,^:;%$', age='3'):
    """Проверяем что можно добавить питомца без фото с названием породы из спецсимволов"""

    _,auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['animal_type'] == animal_type

# 10
def test_successful_add_photo_of_pet(pet_photo_path='images/cat.jpg'):
    """Проверяем успешность запроса на добавление фото питомца по его id"""
    pet_photo_path = os.path.join(os.path.dirname(__file__), pet_photo_path)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if not my_pets['pets']:
        raise Exception("There is no my pets")
    pet_id = my_pets['pets'][0]['id']

    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo_path)

    assert status == 200
    assert result['pet_photo']
