import os
from settings import valid_password, valid_email, invalid_email, invalid_password, invalid_auth_key
from api import PetFriends

pf = PetFriends()


def test_get_auth_key_for_valid_user(email=valid_email, password=valid_password):
    """Метод позволяет проверить, возможно ли получить ключ аутентификации с помощью корректных тестовых данных.
    Ответ приходит со статус-кодом 200 и содержит слово "key"."""

    status, result = pf.get_auth_key(email, password)
    assert status == 200
    assert 'key' in result


def test_add_new_pet_with_valid_data(name='Morda', animal_type='kot', age='3', pet_photo='images/kot_morda.jpg'):
    """Метод позволяет проверить, возможно ли добавить питомца с фото с помощью корректных тестовых данных."""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Запрашиваем ключ аутентификации и сохраняем в переменую auth_key
    _, auth_key = pf.get_auth_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_delete_pet_successfully():
    """Проверяем возможность удаления питомца с корректными тестовыми данными"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_auth_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем, не пустой ли список питомцев. Если пустой, добавляем в него нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "Kat", "4", "images/kot_morda.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем что статус ответа 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_update_pet_info_success(name='Kotya', animal_type='kisa', age=13):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_auth_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Если список не пустой, то пробуем обновить его имя, тип и возраст первого в списке животного по его id
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    # Проверяем, что статус ответа 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
        assert not isinstance(result['age'], int)

    # если спиок питомцев пустой, выкидываем исключение с текстом об отсутствии своих питомцев
    else:
        raise Exception('No pets in My pets')


def test_get_all_pets_with_valid_key():
    """ Проверяем, что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем ключ аутентификации и сохраняем в переменную auth_key.
    Используя этот ключ, запрашиваем список всех питомцев и проверяем, что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' . """

    _, auth_key = pf.get_auth_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, 'my_pets')

    assert status == 200
    assert len(result['pets']) > 0
    print(result)


def test_get_auth_key_with_invalid_password(email=valid_email, password=invalid_password):
    """Метод позволяет проверить, возможно ли получить ключ аутентификации с помощью неправильного пароля.
    Проверяем, что ответ приходит со статус-кодом 403 и не содержит слово "key". """

    status, result = pf.get_auth_key(email, password)
    assert status == 403
    assert 'key' not in result


def test_get_auth_key_with_invalid_username(email=invalid_email, password=valid_password):
    """Метод позволяет проверить, возможно ли получить ключ аутентификации с помощью неправильного пароля.
    Проверяем, что ответ приходит со статус-кодом 403 и не содержит слово "key". """

    status, result = pf.get_auth_key(email, password)
    assert status == 403
    assert 'key' not in result


def test_get_auth_key_with_no_username(email='', password=valid_password):
    """Метод позволяет проверить, возможно ли получить ключ аутентификации с пустым полем ввода логина.
    Проверяем, что ответ приходит со статус-кодом 403 и не содержит слово "key". """

    status, result = pf.get_auth_key(email, password)
    assert status == 403
    assert 'key' not in result


def test_get_auth_key_with_no_password(email=valid_email, password=''):
    """Метод позволяет проверить, возможно ли получить ключ аутентификации с пустым полем ввода логина.
    Проверяем, что ответ приходит со статус-кодом 403 и не содержит слово "key". """

    status, result = pf.get_auth_key(email, password)
    assert status == 403
    assert 'key' not in result


def test_add_new_pet_wrong_photo(name='Morda', animal_type='kot', age='3', pet_photo='images/kot-morda.txt'):
    """Метод позволяет убедиться, что добавить питомца с фото неверного формата невозможно.
    На данный момент обнаруживается баг, поскольку добавляется питомец без фото и ответ приходит со статус-кодом 200."""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_auth_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400
    assert result['name'] != name


def test_add_new_pet_no_photo_success(name='Mordo4ka', animal_type='kotik', age='1'):
    """Проверка возможности добавить питомца без фото.
    Проверяем, что ответ приходит со статус-кодом 200 и содержит слово "name". """
    _, auth_key = pf.get_auth_key(valid_email, valid_password)
    status, result = pf.add_new_pet_no_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_wrong_name(name=911, animal_type='kot', age='3'):
    """Метод позволяет проверить, возможно ли добавить питомца с именем, состоящим из цифр.
    На данный момент обнаруживается баг, питомец с именем из цифр добавляется, приходит ответ со статус-кодом 200,
    а в его теле содержится слово "name". """

    _, auth_key = pf.get_auth_key(valid_email, valid_password)
    status, result = pf.add_new_pet_no_photo(auth_key, name, animal_type, age)
    assert status == 400
    assert result['name'] != name


def test_add_new_pet_wrong_age(name='Kitty', animal_type='cat', age='-3.41', pet_photo='images/kot_morda.jpg'):
    """Метод позволяет убедиться, что невозможно добавить питомца с возрастом, представленным иным числом, чем натуральное.
    На данный момент обнаруживается баг, поскольку добавляется питомец без фото, приходит ответ со статус-кодом 200,
    а в его теле содержится слово "name". """
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_auth_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400
    assert result['name'] != name


def test_add_photo_of_pet_success(pet_photo="images/kot_morda.jpg"):
    """Проверка возможности добавить фото питомца в уже существующую карточку"""

    # Получаем полный путь фото питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_auth_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем, не пустой ли список питомцев. Если пустой, добавляем в него нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_no_photo(auth_key, "Slonik", "Slon", "69")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на добавление фото. Затем снова запрашиваем список питомцев.
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем, что статус ответа 200.
    assert status == 200


def test_delete_pet_with_wrong_id(pet_id='aa8de17e-1214-4072-a7ff-13d5021fbd34aa8de17e-1214-4072-a7ff-13d5021fbd34'):
    """Метод позволяет проверить, что питомца с несуществующим id невозможно удалить.
    На данный момент обнаруживается баг, так как ответ приходит со статус-кодом 200,
    при этом, если в списке были питомцы, никаких изменений не происходит, а если список был пустой, добавляется
    новый питомец с параметрами, заданными через функцию add_new_pet."""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_auth_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем, не пустой ли список питомцев. Если пустой, добавляем в него нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "Kat", "4", "images/kot_morda.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Отправляем запрос на удаление питомца с заведомо неверным id. Затем снова запрашиваем список питомцев.
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем, что ответ приходит со статус-кодом 400.
    assert status == 400


def test_add_new_pet_with_invalid_key(auth_key=invalid_auth_key, name='Morda', animal_type='kot', age='3', pet_photo='images/kot_morda.jpg'):
    """Метод позволяет проверить, возможно ли добавить питомца с помощью несуществующего ключа аутентификации.
    Ответ должен приходить со статус-кодом 403 и в нём не должно содержаться поле "name".
    В данный момент тест проваливается с ошибкой TypeError."""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 403
    assert result['name'] != name