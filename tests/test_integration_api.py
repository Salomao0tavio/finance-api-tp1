"""
Testes de integração: testam os endpoints da API ponta a ponta (HTTP -> service ->
repository -> banco), usando o TestClient do FastAPI com banco em memória.
"""


def test_create_and_get_user(client):
    response = client.post("/users/", json={"name": "Kaio", "email": "kaio@example.com"})
    assert response.status_code == 201
    user_id = response.json()["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["email"] == "kaio@example.com"


def test_create_user_with_invalid_data_returns_400(client):
    response = client.post("/users/", json={"name": "Kaio", "email": "invalido"})
    assert response.status_code == 422  # validado pelo Pydantic (EmailStr)


def test_create_account_for_nonexistent_user_returns_400(client):
    response = client.post(
        "/accounts/", json={"name": "Carteira", "initial_balance": 0.0, "user_id": 999}
    )
    assert response.status_code == 400


def test_create_transaction_and_check_balance(client):
    user = client.post("/users/", json={"name": "Kaio", "email": "kaio@example.com"}).json()
    account = client.post(
        "/accounts/",
        json={"name": "Carteira", "initial_balance": 100.0, "user_id": user["id"]},
    ).json()
    category = client.post("/categories/", json={"name": "Alimentação"}).json()

    response = client.post(
        "/transactions/",
        json={
            "description": "Mercado",
            "amount": 50.0,
            "type": "expense",
            "account_id": account["id"],
            "category_id": category["id"],
        },
    )
    assert response.status_code == 201

    balance_response = client.get(f"/accounts/{account['id']}/balance")
    assert balance_response.status_code == 200
    assert balance_response.json()["balance"] == 50.0  # 100 - 50


def test_delete_user_returns_404_when_not_found(client):
    response = client.delete("/users/9999")
    assert response.status_code == 404
