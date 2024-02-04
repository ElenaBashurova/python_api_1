import requests
from jsonschema import validate
from schems_json import schemas


# Проверка на каждый из методов GET/POST/PUT/DELETE

def test_get():
    response = requests.get('https://reqres.in/api/users/5')
    assert response.status_code == 200


def test_post():
    response = requests.post('https://reqres.in/api/users/5')
    assert response.status_code == 201


def test_put():
    response = requests.put('https://reqres.in/api/users/5')
    assert response.status_code == 200


def test_delete():
    response = requests.delete('https://reqres.in/api/users/5')
    assert response.status_code == 204


# Позитивные/Негативные тесты на одну из ручек

def test_registr_unsuccessful():
    response = requests.post('https://reqres.in/api/register',
                             json={"email": "lindsay.ferguson@reqres.in"})
    assert response.status_code == 400
    body = response.json()
    assert body['error'] == 'Missing password'


def test_registr_successful():
    response = requests.post('https://reqres.in/api/register',
                             json={"email": "eve.holt@reqres.in", "password": "pistol"})
    assert response.status_code == 200
    body = response.json()
    assert body['id'] == 4


# Тесты с ответом и без ответа

def test_users_successful():
    response = requests.put('https://reqres.in/api/users/2',
                            json={"name": "morpheus", "job": "zion resident"})
    assert response.status_code == 200
    body = response.json()
    assert body['name'] == 'morpheus'


def test_user_delete():
    response = requests.delete('https://reqres.in/api/users/5')
    print(response.text)
    assert response.text == ''


# Разные статус-коды 200/201/204/404/400

def test_get_status_kod_200():
    response = requests.get('https://reqres.in/api/users/8')
    assert response.status_code == 200


def test_get_status_kod_201():
    response = requests.post('https://reqres.in/api/users/8')
    assert response.status_code == 201


def test_get_status_kod_204():
    response = requests.delete('https://reqres.in/api/users/8')
    assert response.status_code == 204


def test_get_status_kod_400():
    response = requests.post('https://reqres.in/api/register',
                             json={"email": "lindsay.ferguson@reqres.in"})
    assert response.status_code == 400


def test_get_status_kod_404():
    response = requests.get('https://reqres.in/api/users/35')
    assert response.status_code == 404


# Разные схемы (4-5 схем)

def test_create_user():
    data_user = {'name': 'str', 'job': 'str', 'id': 'str'}
    response = requests.post('https://reqres.in/api/users', data=data_user, verify=False)
    body = response.json()
    validate(body, schema=schemas.create_user)
    assert response.status_code == 201


def test_user():
    data_user = {'email': 'charles.morris@reqres.in', 'first_name': 'Charles', 'last_name': 'Morris'}
    response = requests.get('https://reqres.in/api/users/5', data=data_user, verify=False)
    body = response.json()
    validate(body, schema=schemas.users_single)
    assert response.status_code == 200


def test_registr_user():
    data_user = {"email": "eve.holt@reqres.in", "password": "pistol"}
    response = requests.post('https://reqres.in/api/register', data=data_user, verify=False)
    body = response.json()
    validate(body, schema=schemas.registr_user)
    assert response.status_code == 200


def test_update_user():
    data_user = {"name": "morpheus", "job": "zion resident"}
    response = requests.put('https://reqres.in/api/user/5', data=data_user, verify=False)
    body = response.json()
    validate(body, schema=schemas.update_user)
    assert response.status_code == 200
