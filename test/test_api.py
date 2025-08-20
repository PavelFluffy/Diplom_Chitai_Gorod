import requests
import pytest
import allure
import constants


token = constants.bearer_token
head = {
    "Authorization": constants.bearer_token,
    "Content-Type": "application/json"
    }


@pytest.fixture()
def add():
    """
    Фикстура для:
    добавления книги в корзину,
    получения id книги,
    удаления из корзины после выполнения теста.
    """
    requests.post(
        constants.API_url2,
        headers=head,
        json={"id": 3107612, "adData": {
            "product_shelf": "", "item_list_name": "catalog-page"}})
    resp = requests.get(constants.API_url1,
                        headers=head)
    product_data = resp.json()
    first_product = product_data['products']
    product = first_product[0]
    prod_id = product['id']
    yield prod_id
    requests.delete(
        f'{constants.API_url2}/{prod_id}',
        headers=head)


@allure.suite("API тесты")
@allure.title("Тестирование добавления в корзину")
@allure.description("Тест проверяет корректное добавление в корзину.")
@allure.feature("Добавление в корзину.")
@allure.severity(allure.severity_level.BLOCKER)
def test_add_product_to_cart(add):
    with allure.step("Запрос на товары в корзине"):
        get_cart = requests.get(constants.API_url1,
                                headers=head)
    with allure.step("Получение списка книг"):
        cart = get_cart.json()
        list_book = cart["products"]
    with allure.step("Проверка наличия книги в корзине"):
        assert len(list_book) > 0


@allure.suite("API тесты")
@allure.title("Тестирование изменения количества товара в корзине")
@allure.description("Тест проверяет корректное изменение количества")
@allure.feature("Изменение количества")
@allure.severity(allure.severity_level.CRITICAL)
def test_change_quantity(add):
    with allure.step("Отправка запроса на изменение количества"):
        """
        params:
        id(int) - id продукта, подставляется автоматически после добавления
        quantity(int) - количество
        """
        change = requests.put(constants.API_url1,
                              headers=head,
                              json=[{'id': add, "quantity": 2}])
    with allure.step("Получение количества экзепляров"):
        cart = change.json()
        list_books = cart["products"]
        book = list_books[0]
        quantity = book["quantity"]
    with allure.step("Проверка количества"):
        assert quantity == 2


@allure.suite("API тесты")
@allure.title("Тестирование удаления товара из корзины")
@allure.description("Тест проверяет корректное удаление товара из корзины")
@allure.feature("Удаление из корзины")
@allure.severity(allure.severity_level.CRITICAL)
def test_delete(add):
    with allure.step("Отправка запроса на удаление"):
        deleted = requests.delete(
            f'{constants.API_url2}/{add}',
            headers=head)
    with allure.step("Проверка успешного удаления, код 204"):
        assert deleted.status_code == 204


@allure.suite("API тесты")
@allure.title("Тестирование добавления в корзину с пустым телом")
@allure.description("Тест проверяет корректное добавление в корзину")
@allure.feature("Добавление в корзину")
@allure.severity(allure.severity_level.NORMAL)
def test_add_empty_body():
    with allure.step("Отправка запроса на добавление товара с пустым телом"):
        empty_body = requests.post(
            constants.API_url2,
            headers=head,
            json={})
    with allure.step("Проверка неуспешного запроса, код 422"):
        assert empty_body.status_code == 422


@allure.suite("API тесты")
@allure.title("Тестирование добавления в корзину"
              "другим методом отличным от post")
@allure.description("Тест проверяет корректное добавление в корзину")
@allure.feature("Добавление в корзину")
@allure.severity(allure.severity_level.NORMAL)
def test_add_another_method():
    with allure.step(
         "Отправка запроса на добавление товара""методом отличным от post"):
        another_method = requests.put(
            constants.API_url2,
            headers=head,
            json={"id": 3107612})
    with allure.step("Проверка неуспешного запроса, код 405"):
        assert another_method.status_code == 405
