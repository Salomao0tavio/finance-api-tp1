"""
Teste de aceitação: valida o fluxo completo de uso da aplicação do ponto de vista
do usuário final, garantindo que o sistema atende ao requisito funcional principal
(registrar receitas e despesas e consultar o saldo correto da conta).

Critério de aceite:
"Como usuário, eu quero cadastrar minha conta, registrar uma receita e uma despesa,
e consultar meu saldo atualizado corretamente."
"""


def test_user_can_track_expenses_and_check_final_balance(client):
    # 1. Usuário se cadastra
    user_response = client.post(
        "/users/", json={"name": "Kaio Teixeira", "email": "kaio.teixeira@example.com"}
    )
    assert user_response.status_code == 201
    user = user_response.json()

    # 2. Usuário cria uma conta com saldo inicial
    account_response = client.post(
        "/accounts/",
        json={"name": "Conta Corrente", "initial_balance": 200.0, "user_id": user["id"]},
    )
    assert account_response.status_code == 201
    account = account_response.json()

    # 3. Usuário cria categorias
    salary_category = client.post("/categories/", json={"name": "Salário"}).json()
    food_category = client.post("/categories/", json={"name": "Alimentação"}).json()

    # 4. Usuário registra uma receita (salário)
    income_response = client.post(
        "/transactions/",
        json={
            "description": "Salário de junho",
            "amount": 1500.0,
            "type": "income",
            "account_id": account["id"],
            "category_id": salary_category["id"],
        },
    )
    assert income_response.status_code == 201

    # 5. Usuário registra uma despesa (mercado)
    expense_response = client.post(
        "/transactions/",
        json={
            "description": "Compras do mês",
            "amount": 400.0,
            "type": "expense",
            "account_id": account["id"],
            "category_id": food_category["id"],
        },
    )
    assert expense_response.status_code == 201

    # 6. Usuário consulta o saldo final e confirma que está correto
    balance_response = client.get(f"/accounts/{account['id']}/balance")
    assert balance_response.status_code == 200
    # 200 (inicial) + 1500 (salário) - 400 (mercado) = 1300
    assert balance_response.json()["balance"] == 1300.0

    # 7. Usuário consulta o relatório por categoria
    report_response = client.get(f"/transactions/report/{account['id']}")
    assert report_response.status_code == 200
    report = report_response.json()
    assert report["Salário"]["income"] == 1500.0
    assert report["Alimentação"]["expense"] == 400.0
