class Spider:
    def __init__(self, id, name, keywords):
        self.id = id
        self.name = name
        self.keywords = keywords
        
    def to_dict(self):
        return {
            'id': self.id, 'name': self.name, 'keywords': self.keywords}