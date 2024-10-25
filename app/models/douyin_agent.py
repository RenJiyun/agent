from selenium.webdriver.support.ui import WebDriverWait
from utils.thread import entry_handler, check_timeout, get_remaining_time
from utils.selenium_utils import wait_page_load

STATUS_NOT_LOGIN = 0
STATUS_IN_LIVING_ROOM = 1
STATUS_NOT_IN_LIVING_ROOM = 2

DOUYIN_SELF_URL = "https://www.douyin.com/user/self"
DOUYIN_LIVE_ROOM_URL = "https://live.douyin.com/{}"

# the key cookie name of the login status
# it may not be the key cookie name of the login status, but we use it temporarily to check the login status
DOUYIN_LOGIN_KEY_COOKIE_NAME = "passport_fe_beating_status"


class DouyinAgent:

    def __init__(self, id, driver):
        self._id = id
        # the chrome driver instance of the agent
        self._driver = driver
        self._status = STATUS_NOT_LOGIN
        self._douyin_number = None
        self._username = None
        # the _avatar field is an url of the avatar
        self._avatar = None
        self._douyin_money = None
        self._live_room_id = None
        self._live_room_title = None
        self._anchor_douyin_number = None
        self._anchor_username = None
        self._anchor_avatar = None
        self._danmu_websocket_url = None
        self._flv_pull_url = None

    def to_dict(self):
        """
        convert the agent to a dictionary, 
        so it can let other code use the agent's information

        TODO: now this method just return the id and status of the agent,
              we need to add more information to the dictionary, such as the douyin number, username, avatar, etc.
        """
        return {
            "id": self._id,
            "status": self._status,
            "douyin_number": self._douyin_number,
            "username": self._username,
            "avatar": self._avatar,
            "douyin_money": self._douyin_money,
        }

    def current_url(self):
        """
        get the current url of the agent by using the chrome driver instance
        """
        if self._driver:
            return self._driver.current_url
        else:
            return None

    @entry_handler
    def login(self, timeout):
        """
        login the agent
        it is a blocking method by waiting for the user to login manually,
        we use WebDriverWait to wait for the a flag indicating the user has logged in and process the timeout exception

        login is an entry point, so here we set some context of this thread
            1. the start time of the thread
            2. the remaining time of the thread

        params:
            timeout: the timeout of the operation, it is used to wait for the user to login manually
        """
        
        self._driver.get(DOUYIN_SELF_URL)
        WebDriverWait(self._driver, timeout).until(self._flag_login_success)
        self._status = STATUS_NOT_IN_LIVING_ROOM

        base_info = self._get_agent_info(timeout)
        self._douyin_number = base_info["douyin_number"]
        self._username = base_info["username"]
        self._avatar = base_info["avatar"]
        self._douyin_money = base_info["douyin_money"]


    def _get_agent_info(self, timeout):
        """
        get the information of the agent like douyin number, username, avatar, etc.
        here we use selenium to automatically get the information from the page
        """
        check_timeout(timeout)
        self._driver.get(DOUYIN_SELF_URL)
        wait_page_load(self._driver, get_remaining_time(timeout))
        douyin_number = self._parse_douyin_number()
        username = self._parse_username()
        avatar = self._parse_avatar()
        douyin_money = self._get_douyin_money(timeout)
        return {
            "douyin_number": douyin_number,
            "username": username,
            "avatar": avatar,
            "douyin_money": douyin_money
        }

    
    def _parse_douyin_number(self):
        pass

    def _parse_username(self):
        pass

    def _parse_avatar(self):
        pass

    def _get_douyin_money(self, timeout):
        """
        get the douyin money of the agent
        to get the douyin money, we need to control the selenium to click some buttons 
        and get the information from the page
        """
        pass


    def _flag_login_success(self):
        """
        the flag indicating the user has logged in
        """
        cookies = self._driver.get_cookies()
        for cookie in cookies:
            if cookie["name"] == DOUYIN_LOGIN_KEY_COOKIE_NAME:
                return True
        return False


    def has_logged_in(self):
        """
        check if the agent has logged in
        but it doesn't mean the agent has logged in actually, because the user may logout manually,
        and the status of the agent still remains the same.
        usually, the actual status will be the same as the agent's status, this mean:
            _flag_login_success() == True, then self._status != STATUS_NOT_LOGIN
        """
        return self._status != STATUS_NOT_LOGIN


    @entry_handler
    def enter_live_room(self, live_room_id, timeout):
        """
        enter a live room

        params:
            live_room_id: the id of the live room
        """
        target_url = DOUYIN_LIVE_ROOM_URL.format(live_room_id)
        current_url = self.current_url()
        if current_url == target_url:
            # if the user manually enter the live room, we don't need to enter it again
            # but it will result in the agent's information is not updated
            # anyway, we don't need to do anything here
            return
        self._driver.get(target_url)
        wait_page_load(self._driver, get_remaining_time(timeout))
        self._status = STATUS_IN_LIVING_ROOM
        self._live_room_id = live_room_id
        self._live_room_title = self._parse_live_room_title()
        self._anchor_douyin_number = self._parse_anchor_douyin_number()
        self._anchor_username = self._parse_anchor_username()
        self._anchor_avatar = self._parse_anchor_avatar()
        self._danmu_websocket_url = self._get_danmu_websocket_url(timeout)
        self._flv_pull_url = self._get_flv_pull_url(timeout)
        # TODO: I DON'T KNOW HOW TO PROCESS THE DANMU RANKING LIST


    def _parse_live_room_title(self):
        pass

    def _parse_anchor_douyin_number(self):
        pass

    def _parse_anchor_username(self):
        pass

    def _parse_anchor_avatar(self):
        pass

    def _get_danmu_websocket_url(self, timeout):
        pass

    def _get_flv_pull_url(self, timeout):
        pass
