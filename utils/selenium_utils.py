from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
import socket

"""
this module contains some utils for selenium
"""

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
CHROME_USER_DATA_BASE_DIR = "C:/Users/User/Desktop/selenium/{}"
CHROME_DEBUGGER_BASE_PORT = 9527
CHROME_DRIVER_PATH = "C:/Users/User/Downloads/chromedriver-win64/chromedriver.exe"

def wait_page_load(driver, timeout=10):
    WebDriverWait(driver, timeout).until(lambda d: d.execute_script('return document.readyState') == 'complete')


def get_next_available_port():
    port = CHROME_DEBUGGER_BASE_PORT
    while True:
        try:
            socket.create_connection(("127.0.0.1", port), timeout=1)
            port += 1
        except socket.error:
            return port

def start_chrome_debugger(debugger_port):
    data_dir = CHROME_USER_DATA_BASE_DIR.format(debugger_port)
    os.popen(f"start chrome.exe --remote-debugging-port={debugger_port} --user-data-dir={data_dir}", )


def create_chrome_driver(debugger_port):
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-agent={USER_AGENT}")
    options.add_experimental_option("debuggerAddress", f"127.0.0.1:{debugger_port}")

    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(options=options, service=service)
    return driver
