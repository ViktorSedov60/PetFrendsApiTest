import pytest
import requests
from  settigs import *
import json
import datetime
from datetime import datetime
from api import  PetFriends
import uuid
pf = PetFriends()

@pytest.fixture()
# Получение ключа auth_key
def get_api_keys():
    headers = {'email': valid_email, 'password': valid_password}
    res = requests.get("https://petfriends.skillfactory.ru/api/key", headers=headers)
    optional = res.request.headers

    assert optional.get('email') == valid_email
    assert optional.get('password') == valid_password
    assert res.status_code == 200

    print(res)
    try:
        result = res.json()
    except json.decoder.JSONDecodeError:
        result = res.text
    return result

@pytest.fixture(autouse=True)
def time_delta():
    start_time = datetime.now()
    yield
    end_time = datetime.now()
    print (f"\nТест шел: {end_time - start_time}")

# Фикстуры для Firefox
# @pytest.fixture
# def firefox_options(firefox_options):
#     firefox_options.binary = '/path/to/firefox-bin'
#     firefox_options.add_argument('-foreground')
#     firefox_options.set_preference('browser.anchor_color', '#FF0000')
#     return firefox_options
"""
Где:
firefox_options.binary — путь к exe-драйверу Firefox.
firefox_options.add_argument(‘-foreground’) — возможность запуска в фоновом или реальном режиме. В нашем случае выбран последний. Для фонового укажите ‘-background’.
firefox_options.set_preference(‘borwser.anchor_color’, ‘#FF0000’) — выбор цвета подложки браузера.
"""

# Фикстуры для Chrome
@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.binary_location = '/path/to/chrome'
    chrome_options.add_extension('/path/to/extension.crx')
    chrome_options.add_argument('--kiosk')
    return chrome_options

"""
chrome_options.binary_location — путь к exe браузера (включая сам исполняемый файл).
chrome_options.add_extension — включение дополнений браузера.
"""



# @pytest.fixture(autouse=True)
# def ket_api_key():
#     status, pytest.key = pf.get_api_key(valid_email, valid_password)
#     assert status == 200
#     assert 'key' in pytest.key
#
#     yield
#
#     assert pytest.status == 200

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # This function helps to detect that some test failed
    # and pass this information to teardown:

    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep

@pytest.fixture
def web_browser(request, selenium):

    browser = selenium
    browser.set_window_size(1400, 1000)

    # Return browser instance to test case:
    yield browser

    # Do teardown (this code will be executed after each test):

    if request.node.rep_call.failed:
        # Make the screen-shot if test failed:
        try:
            browser.execute_script("document.body.bgColor = 'white';")

            # Make screen-shot for local debug:
            browser.save_screenshot('screenshots/' + str(uuid.uuid4()) + '.png')

            # For happy debugging:
            print('URL: ', browser.current_url)
            print('Browser logs:')
            for log in browser.get_log('browser'):
                print(log)

        except:
            pass # just ignore any errors here