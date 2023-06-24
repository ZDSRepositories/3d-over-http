import vpython, requests

EXPECTED_PROPERTIES = ['id', 'script', 'pos', 'name', 'color']

class Entity:
    def __init__(self, eid=None, name=None, pos=None, color=None, script=None, created_at= None, modified_at = None):
        self.modified_at = modified_at
        self.created_at = created_at
        self.script = script
        self.pos = pos
        self.name = name
        self.eid = eid

        self.body = None
    def realize(self, entity_json):
        self.eid = entity_json["id"]
        self.script = entity_json["script"]
        self.pos = entity_json["pos"]
        self.color = entity_json["color"]
        self.name = entity_json["name"]

        #self.body =
