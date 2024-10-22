import socket
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from app.models.zhihu_event import Event
from selenium.webdriver.chrome.service import Service
import traceback
import time
import logging
import os
import random


# logging.basicConfig(level=logging.DEBUG)

os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['NO_PROXY'] = '*'

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
chrome_user_data_dir = r"C:/Users/User/Desktop/selenium"
chrome_debugger_port = 9527


def _wait_for_page_load(driver, timeout=10):
    """
    Wait for the page to load, wait all the JavaScript to finish executing

    Parameters:
        driver: the driver to wait for
    """
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    )

def _scroll_down(driver, sleep_duration_range=(0.5, 1)):
    """
    Scroll down the page and return whether we've reached the bottom of the page

    Parameters:
        driver: the driver to scroll down
        sleep_duration_range: the range of the sleep duration

    Returns:
        bool: whether we've reached the bottom of the page
    """
    driver.execute_script("window.scrollBy(0, 300);")
    sleep_duration = random.uniform(sleep_duration_range[0], sleep_duration_range[1])
    time.sleep(sleep_duration)
    


def _is_bottom_of_page(driver, threshold=10):
    """
    Check if we've reached the bottom of the page

    Parameters:
        driver: the driver to check
        threshold: the threshold of the scroll position
    """
    current_scroll = driver.execute_script("return window.pageYOffset;")
    total_height = driver.execute_script("return document.documentElement.scrollHeight;")
    viewport_height = driver.execute_script("return window.innerHeight;")
    print(f"current_scroll: {current_scroll}, total_height: {total_height}, viewport_height: {viewport_height}")
    return current_scroll >= total_height - threshold
    

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

    service = Service("C:/Users/User/Downloads/chromedriver-win64/chromedriver.exe")
    driver = webdriver.Chrome(options=options, service=service)
    return driver


def _wait_for_login(driver, is_logged_in_func, timeout=120):
    WebDriverWait(driver, timeout).until(is_logged_in_func)


def _print_stack_trace():
    print(traceback.format_exc())


_zhihu_index_url = "https://www.zhihu.com"
_zhihu_profile_url = "https://www.zhihu.com/people/{}"

_drivers: dict[str, webdriver.Chrome] = {}

class ZhihuService:

    @staticmethod
    def login(username: str, timeout=120):
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
            _wait_for_page_load(driver)
            _wait_for_login(driver, ZhihuService._is_logged_in)
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
    def get_user_info(username: str, timeout=10):
        if not _check_chrome_debugger_running():
            return {"status": 0, "msg": "Chrome debugger not running, try to login first"}
        
        driver = _drivers.get(username)
        if driver is None:
            return {"status": 0, "msg": "User not logged in"}
        
        driver.get(_zhihu_profile_url.format(username))
        _wait_for_page_load(driver)
        return {"status": 1, "msg": "success"}
        

    @staticmethod
    def get_user_events(username: str, from_time: str, to_time: str, timeout=10):
        if not _check_chrome_debugger_running():
            return {"status": 0, "msg": "Chrome debugger not running, try to login first"}
        
        driver = _drivers.get(username)
        if driver is None:
            return {"status": 0, "msg": "User not logged in"}
        
        driver.get(_zhihu_profile_url.format(username))
        _wait_for_page_load(driver)
        event_list = ZhihuService._get_user_events(driver, from_time, to_time)
        return {"status": 1, "msg": "success", "total": len(event_list), "data": [event.to_dict() for event in event_list]}
    

    @staticmethod
    def _get_user_events(driver, from_time: str, to_time: str):
        ZhihuService._scroll_down_until_time_from(driver, from_time)
        event_list = ZhihuService._get_event_list(driver)
        return event_list
    

    @staticmethod
    def _scroll_down_until_time_from(driver, from_time: str):
        """
        Scroll down the page until the last event time is less than the from_time or we've reached the bottom of the page
        """
        while True:
            last_event_time = ZhihuService._get_last_event_time(driver)
            print(last_event_time)
            if last_event_time < from_time:
                break
            
            _scroll_down(driver)
            if _is_bottom_of_page(driver):
                break
            
    
    @staticmethod
    def _get_last_event_time(driver):
        profile_activities_div = driver.find_element(By.ID, "Profile-activities")
        children = profile_activities_div.find_elements(By.XPATH, "./*")        

        list_container_div = children[1]

        WebDriverWait(driver, 10).until(
            ZhihuService._is_event_list_loaded
        )
        
        children = list_container_div.find_elements(By.XPATH, "./*")
        event_div_list = children[1:-1]
        last_event_div = event_div_list[-1]
        last_event = ZhihuService._parse_event(last_event_div)
        return last_event.event_time
    

    @staticmethod
    def _is_event_list_loaded(driver):
        profile_activities_div = driver.find_element(By.ID, "Profile-activities")
        children = profile_activities_div.find_elements(By.XPATH, "./*")
        list_container_div = children[1]
        children = list_container_div.find_elements(By.XPATH, "./*")
        return len(children) > 2

    @staticmethod
    def _get_event_list(driver):
        profile_activities_div = driver.find_element(By.ID, "Profile-activities")
        children = profile_activities_div.find_elements(By.XPATH, "./*")        

        list_container_div = children[1]

        children = list_container_div.find_elements(By.XPATH, "./*")
        event_div_list = children[1:-1]
        event_list = [ZhihuService._parse_event(event_div, print_result=True) for event_div in event_div_list]
        return event_list

    @staticmethod
    def _parse_event(event_div, print_result=False):
        children = event_div.find_elements(By.XPATH, "./*")
        list_item_meta_div = children[0]
        event_type, event_time = ZhihuService._parse_event_meta(list_item_meta_div)
        list_item_content_div = children[1]
        result = Event(event_type, event_time)
        if print_result:
            print(result)
        return result
    
    @staticmethod
    def _parse_event_meta(list_item_meta_div):
        children = list_item_meta_div.find_elements(By.XPATH, "./*")
        activity_item_meta = children[0]
        children = activity_item_meta.find_elements(By.XPATH, "./*")
        event_type = children[0].text
        event_time = children[1].text
        return event_type, event_time
        
