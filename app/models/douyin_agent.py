from selenium.webdriver.support.ui import WebDriverWait

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
        }

    def current_url(self):
        """
        get the current url of the agent by using the chrome driver instance
        """
        if self._driver:
            return self._driver.current_url
        else:
            return None


    def login(self, timeout):
        """
        login the agent
        it is a blocking method by waiting for the user to login manually,
        we use WebDriverWait to wait for the a flag indicating the user has logged in and process the timeout exception

        params:
            timeout: the timeout of the operation, it is used to wait for the user to login manually
        """
        self._driver.get(DOUYIN_SELF_URL)
        WebDriverWait(self._driver, timeout).until(self._flag_login_success)


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
