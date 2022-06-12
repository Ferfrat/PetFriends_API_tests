import json
import requests

from requests_toolbelt.multipart.encoder import MultipartEncoder

class PetFriends:
    """Библиотека c API запросами к сайту Pet Friends"""

    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru/'

    def get_api_key(self, email: str, password: str) -> json:
        """Get-запрос к API  сервера с валидными мейлом и паролем в headers,
        который возвращает код статуса запроса и уникальный ключ в формате JSON"""
        headers = {
            'email': email,
            'password': password,
        }
        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str = "") -> json:
        """Метод делает get запрос к API сервера с уникальным ключом пользователя в headers и
          пустым  значением в filter и возвращает: код статуса запроса и список
          всех питомцев в формате Json либо в виде строки. Для получения списка только своих
          питомцев filter должен иметь значение my_pets """
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str) -> json:
        """Метод отправляет POST запрос к API, добавляет данные о новом питомце на сайт и
        возвращает код статуса запроса и результат в формате JSON с данными добавленного нами питомца. """

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Метод делает DELETE запрос к API сайта, удоляет питомца по его ID и возвращает
        статус запроса, а также должен приходить результат в формате JSON с текстом уведомления
        об успешном удалении питомца из базы"""
        headers = {
            'auth_key': auth_key['key'],
            'pet_id': pet_id
        }

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: str) -> json:
        """Отправляем PUT запррс к API сайта, который изменяет данные питомца с указанным ID и возвращает
        код статуса запроса и измененные данные о питомце в формате JSON"""
        headers = {
            'auth_key': auth_key['key'],
            'pet_id': pet_id
        }
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_new_pet_without_photo(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        """Метод делает POST запрос к API с данными на добавляемого питомца (без фото) и возвращает статус
        запроса на сервер и результат в формате JSON с данными добавленного питомца"""

        headers = {
            'auth_key': auth_key['key'],
        }
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_photo_of_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Метод делает POST запрос к API сервера и добавляет новое фото указанного
        к данным питомца с указанным ID. Возвращает код статуса запроса и результат
        в формате JSON с информацией о животном."""
        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {
            'auth_key': auth_key['key'],
            'Content-Type': data.content_type
        }

        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)

        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result
