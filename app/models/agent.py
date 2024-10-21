from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from utils.living_room import get_stream_data

class Agent:
    def __init__(self, id, driver):
        self.id = id
        self.driver = driver
        self.current_url = None
        self.username = None
        self.avatar = None,
        self.is_in_living_room = False,
        self.living_room_id = None,
        self.flv_pull_url = None,
        self.anchor_name = None,
        self.__danmu_input = None,
        self.__like_button = None,
        self.__create_time = None
        
    def to_dict(self):
        return {
            'id': self.id,
            'driver': self.driver,
            'current_url': self.current_url,
            'username': self.username,
            'avatar': self.avatar,
            'is_in_living_room': self.is_in_living_room,
            'living_room_id': self.living_room_id,
            'flv_pull_url': self.flv_pull_url,
            'create_time': self.__create_time,
            'anchor_name': self.anchor_name
        }
    
    def init(self, timeout=120):
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda x: self._is_initialized()
            )
            self.__create_time = datetime.now()
        except TimeoutException:
            raise Exception(f"Agent initialization timed out after {timeout} seconds")

    def _is_initialized(self):
        # 通过检查某个cookie是否存在来判断是否初始化完成
        # TODO
        pass
    
    def enter_living_room(self, room_id, timeout=120):
        url = f'https://live.douyin.com/{room_id}'
        self.driver.get(url)
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda x: self._is_in_living_room()
            )
            self.is_in_living_room = True
            self.living_room_id = room_id
            self.current_url = url
            self.flv_pull_url = self._get_flv_pull_url(url)
            self.__danmu_input = self._get_danmu_input(url)
            self.__like_button = self._get_like_button(url)
            self.danmu_ws = self._get_danmu_ws(url)
        except TimeoutException:
            raise Exception(f"Agent entering living room timed out after {timeout} seconds")
    
    def _is_in_living_room(self):
        # 通过校验某个元素是否存在来判断是否在直播间
        # TODO
        pass
    
    def _get_flv_pull_url(self, url):
        stream_data = get_stream_data(url)
        if stream_data:
            # 总是获取原画画质
            return stream_data['ORIGIN']
        else:
            return None
    
    def _get_danmu_input(self, url):
        pass
    
    def _get_like_button(self, url):
        pass
    
    def _get_danmu_ws(self, url):
        # 获取弹幕的websocket地址
        pass
    
    def leave_living_room(self):
        self.driver.get('https://www.douyin.com')
        self.is_in_living_room = False
        self.living_room_id = None
        self.flv_pull_url = None
        self.__danmu_input = None
        self.__like_button = None
        
    
    def send_danmu(self, content):
        if self.is_in_living_room:
            self._do_send_danmu(content)
        else:
            raise Exception('Agent is not in a living room')
    
    def _do_send_danmu(self, content):
        pass
    
    def send_gift(self, name, count):
        pass
    
    def like(self, frequency, duration):
        pass