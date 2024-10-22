import socket
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import traceback
import time
import logging
import os


logging.basicConfig(level=logging.DEBUG)

os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['NO_PROXY'] = '*'

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
chrome_user_data_dir = r"C:/Users/User/Desktop/selenium"
chrome_debugger_port = 9527


def timeout_handler(func):
    def wrapper(*args, **kwargs):
        start_time = kwargs.get('start_time')
        total_timeout = kwargs.get('total_timeout')
        remaining_time = _remaining_time(start_time, total_timeout)
        return func(*args, **kwargs, remaining_time=remaining_time)
    return wrapper


def timeout_entry_handler(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        total_timeout = kwargs.get('timeout')
        return func(*args, **kwargs, start_time=start_time, total_timeout=total_timeout)
    return wrapper


def _remaining_time(start_time, total_timeout):
    _remaining_time = total_timeout - (time.time() - start_time)
    if _remaining_time <= 0:
        raise Exception("Operation timed out")
    return _remaining_time


@timeout_handler
def _wait_for_page_load(driver, start_time=None, total_timeout=None, remaining_time=None):
    """
    Wait for the page to load, wait all the JavaScript to finish executing

    Parameters:
        driver: the driver to wait for
        start_time: the start time of the operation
        total_timeout: the total timeout of the operation
    """
    WebDriverWait(driver, remaining_time).until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    )

def _start_chrome_debugger():
    os.popen(f"start chrome.exe --remote-debugging-port={chrome_debugger_port} --user-data-dir={chrome_user_data_dir}")

def _check_chrome_debugger_running():
    """
    Check if the chrome debugger is running by checking the debugger port
    """ 
    try:
        socket.create_connection(("127.0.0.1", chrome_debugger_port), timeout=1)
        return True
    except socket.error:
        return False

def _get_chrome_driver():
    """
    Get a chrome driver
    """
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-agent={user_agent}")
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
    driver = webdriver.Chrome(options=options)
    return driver


@timeout_handler
def _wait_for_login(driver, is_logged_in_func, start_time=None, total_timeout=None, remaining_time=None):
    WebDriverWait(driver, remaining_time).until(is_logged_in_func)


def _print_stack_trace():
    print(traceback.format_exc())


_zhihu_index_url = "https://www.zhihu.com"
_zhihu_profile_url = "https://www.zhihu.com/people/{}"

_drivers: dict[str, webdriver.Chrome] = {}

class ZhihuService:

    @staticmethod
    @timeout_entry_handler
    def login(username: str, timeout=120, start_time=None, total_timeout=None):
        """
        Login to zhihu

        Parameters:
            username: the username of the user
            timeout: the timeout of the operation
        """
        try:
            driver = _drivers.get(username)
            if driver is not None:
                if _check_chrome_debugger_running():
                    return {"status": 0, "msg": "User already logged in"}
                else:
                    driver.quit()
                    _drivers.pop(username, None)

            _start_chrome_debugger()
            time.sleep(1)
            driver = _get_chrome_driver()
            _drivers[username] = driver

            driver.get(_zhihu_index_url)
            _wait_for_page_load(driver, start_time=start_time, total_timeout=total_timeout)
            _wait_for_login(driver, ZhihuService._is_logged_in, start_time=start_time, total_timeout=total_timeout)
        except Exception as e:
            _print_stack_trace()
            driver = _drivers.pop(username, None)
            if driver is not None:
                driver.quit()
            return {"status": 0, "msg": f"Login failed: {str(e)}"}

        return {"status": 1, "msg": "success"}

    


    @staticmethod
    def _is_logged_in(driver):
        """
        Check if the user is logged in manually
        The flag is the cookie has the key "z_c0"
        """
        cookies = driver.get_cookies()
        for cookie in cookies:
            if cookie['name'] == 'z_c0':
                return True
        return False


    @staticmethod
    def logout(username: str):
        driver = _drivers.pop(username, None)
        if driver is None:
            return {"status": 0, "msg": "User not logged in"}
        driver.quit()
        return {"status": 1, "msg": "success"}
    

    @staticmethod
    @timeout_entry_handler
    def get_user_info(username: str, timeout=10, start_time=None, total_timeout=None):
        if not _check_chrome_debugger_running():
            return {"status": 0, "msg": "Chrome debugger not running, try to login first"}
        
        driver = _drivers.get(username)
        if driver is None:
            return {"status": 0, "msg": "User not logged in"}
        
        driver.get(_zhihu_profile_url.format(username))
        _wait_for_page_load(driver, start_time=start_time, total_timeout=total_timeout)
        return {"status": 1, "msg": "success"}
        
