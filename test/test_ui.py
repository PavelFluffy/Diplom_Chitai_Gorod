import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
import constants


@pytest.fixture(scope="function")
def driver():
    """
    Фикстура для инициализации и завершения работы драйвера.
    Открытия окна на полный экран.
    Открытия сайта магазина.
    """
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.get(constants.UI_url)
    yield driver
    driver.quit()


@allure.suite("UI тесты")
@allure.title("Тестирование добавления в корзину")
@allure.description("Тест проверяет корректное добавление в корзину."
                    "Наличие товара в корзине.")
@allure.feature("Добавление в корзину.")
@allure.severity(allure.severity_level.BLOCKER)
def test_add_product_to_cart(driver):
    with allure.step("Наведение и переход в карточку товара"):
        first_product = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, ".product-card__caption a")))
        first_product.click()
    # Ожидание загрузки деталей страницы:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((
        By.CSS_SELECTOR, ".product-detail-page")))
    with allure.step("Добавление товара в корзину"):
        add_to_cart = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'button[class*="product-buttons__main-action"]')))
        add_to_cart.click()
    # Ожидание появления индикатора:
    porduct_indicator = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.CSS_SELECTOR, 'div[class*="chg-indicator"]')))
    with allure.step("Проверка на появление индикатора добавления в корзину"):
        assert porduct_indicator.text == "1"


@allure.suite("UI тесты")
@allure.title("Тестирование удаления товара из корзины")
@allure.description("Тест проверяет корректное удаление товара из корзины")
@allure.feature("Удаление из корзины")
@allure.severity(allure.severity_level.CRITICAL)
def test_deleted_product(driver):
    with allure.step("Наведение и переход в карточку товара"):
        first_product = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, ".product-card__caption a")))
        first_product.click()
    # Ожидание загрузки деталей страницы:
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((
        By.CSS_SELECTOR, ".product-detail-page")))
    with allure.step("Добавление товара в корзину"):
        add_to_cart = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'button[class*="product-buttons__main-action"]')))
        add_to_cart.click()

    with allure.step("Переход в корзину"):
        go_cart = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'button[class*="chg-app-button--green product-buttons"]')))
        go_cart.click()

    with allure.step("Удаление товара"):
        deleted = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, 'button[class*="cart-item__delete-button"]')))
        deleted.click()
    # Ожидание удаления товара:
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((
        By.CSS_SELECTOR, ".cart-item-deleted__title")))
    # Нахождение заголовка с кол-ом товара в корзине:
    item_in_cart = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((
            By.CSS_SELECTOR, '.info-item__title')))
    with allure.step("Проверка на отсутствие товара в корзине"):
        assert item_in_cart.text == "0 товаров"


@allure.suite("UI тесты")
@allure.title("Тестирование восстановления удаленного товара")
@allure.description("Тест проверяет корректное восстановление удаленного"
                    "товара")
@allure.feature("Восстановление товара")
@allure.severity(allure.severity_level.NORMAL)
def test_return_product_in_cart(driver):
    with allure.step("Наведение и переход в карточку товара"):
        first_product = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, ".product-card__caption a")))
        first_product.click()
    # Ожидание загрузки деталей страницы:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((
        By.CSS_SELECTOR, ".product-detail-page")))
    with allure.step("Добавление товара в корзину"):
        add_to_cart = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'button[class*="product-buttons__main-action"]')))
        add_to_cart.click()

    with allure.step("Переход в корзину"):
        go_cart = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'button[class*="chg-app-button--green product-buttons"]')))
        go_cart.click()

    with allure.step("Удаление товара"):
        deleted = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, 'button[class*="cart-item__delete-button"]')))
        deleted.click()
    # Ожидание удаления товара:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((
        By.CSS_SELECTOR, ".cart-item-deleted__title")))

    with allure.step("Восстановление продукта"):
        return_propduct = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'button[class*="cart-item-deleted__button"]')))
        return_propduct.click()

    # Ожидание загрузки восстановления товара:
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((
            By.CSS_SELECTOR, '.cart-page__title--append'), "1 товар"))
    item_in_cart = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.CSS_SELECTOR, '.cart-page__title--append')))
    with allure.step("Проверка на восстановление товара"):
        assert item_in_cart.text == "1 товар"


@allure.suite("UI тесты")
@allure.title("Тестирование изменения количества товара в корзине")
@allure.description("Тест проверяет корректное изменение количества")
@allure.feature("Изменение количества")
@allure.severity(allure.severity_level.CRITICAL)
def test_change_quantity(driver):
    with allure.step("Наведение и переход в карточку товара"):
        first_product = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, ".product-card__caption a")))
        first_product.click()
    # Ожидание загрузки деталей страницы:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((
        By.CSS_SELECTOR, ".product-detail-page")))
    with allure.step("Добавление товара в корзину"):
        add_to_cart = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'button[class*="product-buttons__main-action"]')))
        add_to_cart.click()

    with allure.step("Переход в корзину"):
        go_cart = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'button[class*="chg-app-button--green product-buttons"]')))
        go_cart.click()

    with allure.step("Изменение количества на +1"):
        change_quantity = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'svg[class*="chg-ui-input-number__input-control--increment"]'
                )))
        change_quantity.click()
    # Нахождение поля с указанием количества:
    quantity_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.CSS_SELECTOR, 'input[class*="chg-app-input__control"]')))
    # Получение атрибута количества:
    quantity = quantity_field.get_attribute("value")
    with allure.step("Проверка на колечство товара в корзине = 2"):
        assert quantity == '2'


@allure.suite("UI тесты")
@allure.title("Тестирование поиска товара по названию")
@allure.description("Тест проверяет корректный поиск товара с помощью"
                    "поисковой строки")
@allure.feature("Поисковая строка")
@allure.severity(allure.severity_level.CRITICAL)
def test_search_for_title(driver):
    with allure.step("Ввод названия и подтверждение поиска"):
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, 'input[class*="search-form__input"]')))
        search_box.send_keys("Вий")
        search_box.send_keys(Keys.RETURN)

    # Ожидание закгруки найденных результатов:
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((
        By.CSS_SELECTOR, ".chg-app-tab")))

    with allure.step("Выбор первого результата и получение атрибута названия"):
        title_book = driver.find_element(
            By.CSS_SELECTOR, 'a[class="product-card__title"]')
        title_name = title_book.get_attribute("title")

    with allure.step("Проверка на содержания запроса в название"):
        assert "Вий" in title_name
