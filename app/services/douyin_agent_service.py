from app.models.douyin_agent import DouyinAgent
from utils.selenium_utils import wait_page_load
from utils.stack_trace import print_stack_trace
from utils.selenium_utils import get_next_available_port, start_chrome_debugger, create_chrome_driver
import json
import time


class DouyinAgentService:
    """
    control douyin agent to execute tasks
    tasks:
        1. create a new agent
        2. login
        3. enter a live room
        4. leave a live room
        5. send message
        6. give gift
        7. like
        8. get the danmu ranking list periodically if the agent is in a live room

    now the agent has three status:
        1. not login
        2. in a live room
        3. not in a live room
    
    if the agent is in the login status, it can get the information below:
        1. the douyin number
        2. the username
        3. the avatar
        4. the douyin money it has

    if the agent is in the in a live room status, it can get the information below together with the login information:
        1. the live room id
        2. the live room title
        3. the live room anchor's douyin number
        4. the live room anchor's username
        5. the live room anchor's avatar
        6. the danmu message websocket url
        7. the live pull url
        8. the danmu ranking list
    
    ATTENTION: 
        1. ALL THE METHODS IN THIS CLASS ARE STATIC METHODS
        2. ALL THE PUBLIC METHODS WILL RETURN A DICT, NOT A OBJECT
           THE DICT CONTAINS THREE KEYS:
              1. status: the status of the operation, 0 for success, other values for failure, but now only 0 and 1 are used
              2. msg: the message of the operation, it will be empty if the status is 0
              3. data: the data of the operation, it will be empty if the status is 0
              4. total: the total number of the data if the data is a list something like a ranking list
                        and this filed exists only when the data is a list
        3. ALL THE PUBLIC METHODS WILL PROCESS THE EXCEPTION. FOR NOW WE JUST PRINT THE STACK TRACE,
           AND GET THE ERROR MESSAGE, THEN RETURN THE DICT CONTAINING THE STATUS AND THE MSG
    """

    # the global sequence number of the agent
    _id = 0
    # the global map of the agent, the key is the id, the value is the agent instance
    _agents = {}
    
    @staticmethod
    def create():
        """
        create a new agent
        create a new chrome driver instance, and assign a new id to the agent,
        the id is just a global sequence number of this class, and it will be increased by 1 when a new agent is created,
        then the new agent will be kept in a global map, the key is the id, the value is the agent instance,
        so the other operations can get the agent instance by the id
        """
        driver = DouyinAgentService._get_new_driver()
        id = DouyinAgentService._get_new_id()
        agent = DouyinAgent(id, driver)
        DouyinAgentService._agents[id] = agent
        return {"status": 0, "data": agent.to_dict()}


    @staticmethod
    def _get_new_id():
        DouyinAgentService._id += 1
        return DouyinAgentService._id
    

    @staticmethod
    def _get_new_driver():
        """
        create a new chrome driver instance
        actually, create a new chrome driver instance is a common operation, we can put it in a common module,
        but it may need some special configurations, anyway, it's not a big deal, so I put it here
        """
        debugger_port = get_next_available_port()
        start_chrome_debugger(debugger_port)
        return create_chrome_driver(debugger_port)
    

    @staticmethod
    def login(agent_id, timeout):
        """
        login the agent

        params:
            agent_id: the id of the agent
            timeout: the timeout of the operation, it is used to wait for the user to login manually
        """
        agent = DouyinAgentService._agents[agent_id]
        if agent is None:
            return {"status": 1, "msg": "agent not found"}
        
        if agent.has_logged_in():
            return {"status": 0, "data": agent.to_dict()}
        
        try:
            agent.login(timeout)
        except Exception as e:
            print_stack_trace(e)
            return {"status": 1, "msg": str(e)}

        return {"status": 0, "data": agent.to_dict()}
        

    _debug_driver = None

    @staticmethod
    def debug1():
        """
        create a new temporary chrome driver instance
        """
        if DouyinAgentService._debug_driver is None:
            DouyinAgentService._debug_driver = DouyinAgentService._get_new_driver()
        
        DouyinAgentService._debug_driver.get("https://www.douyin.com/user/self")
        wait_page_load(DouyinAgentService._debug_driver)
        cookies = DouyinAgentService._debug_driver.get_cookies()
        # save the cookies to a file named cookies_login_before.json
        with open("cookies_login_before.json", "w") as f:
            json.dump(cookies, f)
        return

    @staticmethod
    def debug2():
        # sleep 1 minute to wait for the user to login
        cookies = DouyinAgentService._debug_driver.get_cookies()
        # save the cookies to a file named cookies_login_after.json
        with open("cookies_login_after.json", "w") as f:
            json.dump(cookies, f)
        return

    @staticmethod
    def debug3():
        cookies = DouyinAgentService._debug_driver.get_cookies()
        # save the cookies to a file named cookies_logout.json
        with open("cookies_logout.json", "w") as f:
            json.dump(cookies, f)
        return
