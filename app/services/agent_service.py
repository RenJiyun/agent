from app.models.agent import Agent
from selenium import webdriver
import traceback

class AgentService:
    
    last_id: int = 0
    agent_map: dict = {}
    
    @staticmethod
    def get_all():
        return {
            "status": 1, 
            "msg": "success", 
            "data": list(AgentService.agent_map.values()), 
            "total": len(AgentService.agent_map)
        }

    @staticmethod
    def get_by_id(agent_id):
        if agent_id in AgentService.agent_map:
            agent = AgentService.agent_map[agent_id]
            return {"status": 1, "msg": "success", "data": agent.to_dict()}
        else:
            return {"status": 0, "msg": "agent not found"}

    
    @staticmethod
    def create(data):
        AgentService.last_id += 1
        new_id = AgentService.last_id
        
        # 创建driver
        # TODO 还需设置其他参数
        driver = webdriver.Chrome()
        agent = Agent(id=new_id, driver=driver)
        
        # 等待agent初始化, 超时时间为两分钟
        try:
            agent.init(timeout=120)
            AgentService.agent_map[new_id] = agent
        except Exception as e:
            print("Agent initialization failed. Exception details:")
            print(traceback.format_exc())
            driver.quit()
            return {"status": 0, "msg": str(e)}
        return {"status": 1, "msg": "success", "data": agent.to_dict()}
    
    
    @staticmethod
    def delete(agent_id):
        if agent_id in AgentService.agent_map:
            agent = AgentService.agent_map[agent_id]
            agent.driver.quit()
            del AgentService.agent_map[agent_id]
            return {"status": 1, "msg": "success"}
        else:
            return {"status": 0, "msg": "agent not found"}

    @staticmethod
    def enter_living_room(agent_id, room_id):
        if agent_id in AgentService.agent_map:
            agent = AgentService.agent_map[agent_id]
            try:
                agent.enter_living_room(room_id, timeout=120)
            except Exception as e:
                print(f"Failed to enter living room. Exception details:")
                print(traceback.format_exc())
                return {"status": 0, "msg": str(e)}
            return {"status": 1, "msg": "success"}
        else:
            return {"status": 0, "msg": "agent not found"}

    @staticmethod
    def leave_living_room(agent_id):
        if agent_id in AgentService.agent_map:
            agent = AgentService.agent_map[agent_id]
            agent.leave_living_room()
            return {"status": 1, "msg": "success"}
        else:
            return {"status": 0, "msg": "agent not found"}

    @staticmethod
    def send_danmu(agent_id, content):
        if agent_id in AgentService.agent_map:
            agent = AgentService.agent_map[agent_id]
            agent.send_danmu(content)
            return {"status": 1, "msg": "success"}
        else:
            return {"status": 0, "msg": "agent not found"}

    @staticmethod
    def send_gift(agent_id, name, count):
        if agent_id in AgentService.agent_map:
            agent = AgentService.agent_map[agent_id]
            agent.send_gift(name, count)
            return {"status": 1, "msg": "success"}
        else:
            return {"status": 0, "msg": "agent not found"}

    @staticmethod
    def like(agent_id, frequency, duration):
        if agent_id in AgentService.agent_map:
            agent = AgentService.agent_map[agent_id]
            agent.like(frequency, duration)
            return {"status": 1, "msg": "success"}
        else:
            return {"status": 0, "msg": "agent not found"}
