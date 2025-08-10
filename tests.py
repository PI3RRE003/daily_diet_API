import requests
import pytest
from datetime import datetime
#pytest -v  tests.py rodar testes

BASE_URL = 'http://127.0.0.1:5000'
meals = []

def test_create_meal():
    new_meal_data = {
    "name_meal" : "almoço em familia completo",#sempre renomear para o teste passar
    "description" : "teste",
    "diet_or_not" : "Sim"
    }
    response = requests.post(f"{BASE_URL}/meal", json=new_meal_data)
    assert response.status_code == 200
    response_json = response.json()
    assert "message" in response_json
    assert "id" in response_json
    meals.append(response_json['id'])

def  test_get_meal():
    if meals:
        meals_id = meals[0]
        response = requests.get(f'{BASE_URL}/meals/{meals_id}')
        assert response.status_code == 200
        response_json = response.json()
        assert meals_id == response_json['id']

def test_get_meals():
    response = requests.get(f'{BASE_URL}/meals')
    assert response.status_code == 200 
    response_json = response.json()
    for meal in response_json:
        assert "id" in meal
        assert "name_meal" in meal
        assert "description" in meal
        assert "date_time" in meal
        assert "diet_or_not" in meal

def test_update_meal():
    if meals:
        meals_id = meals[0]
        formatted = datetime.now().strftime("%d/%m/%Y %H:%M")
        date_time = formatted

        payload = {
            "name_meal" : "Café e bolacha e pão e cuscuz",
            "description" : "Café levemente adoçado com bolacha agua e sal",
            "date_time" : date_time,
            "diet_or_not" : "sim"
        }

        response = requests.put(f"{BASE_URL}/meals/{meals_id}", json=payload)
        response.status_code == 200
        response_json = response.json()
        assert "message" in response_json
        

        response = requests.get(f'{BASE_URL}/meals/{meals_id}')
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['name_meal'] == payload['name_meal']
        assert response_json['description'] == payload['description']
        assert response_json['diet_or_not'] == payload['diet_or_not']

def test_delete_meal():
    if meals:
        meal_id = meals[0]
        response = requests.delete(f'{BASE_URL}/meals/{meal_id}') 
        response.status_code == 200
        
        response = requests.get(f'{BASE_URL}/meals/{meal_id}')
        assert response.status_code == 404