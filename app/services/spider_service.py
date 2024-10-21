from app.models.spider import Spider

class SpiderService:
    last_id: int = 0
    spider_map: dict = {}
    
    @staticmethod
    def get_all():
        pass
    
    @staticmethod
    def get_by_id(spider_id):
        pass
    
    @staticmethod
    def create(name, keywords):
        SpiderService.last_id += 1
        new_id = SpiderService.last_id
        spider = Spider(id=new_id, name=name, keywords=keywords)
        
        SpiderService.spider_map[new_id] = spider
        return spider.to_dict()