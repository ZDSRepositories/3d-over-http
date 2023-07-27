import vpython, requests, json
from threecommon import *
from concurrent.futures import ThreadPoolExecutor # workaround for python concurrency bug

HOST_NAME, HOST_PORT = "localhost", 80
EXPECTED_PROPERTIES = ['id', 'script', 'pos', 'name', 'color']
WORLD = []

vpython.scene.title = f"remote sim at {HOST_NAME}:{HOST_PORT}"

def fetch_world():
    r = requests.get(f"http://{HOST_NAME}:{HOST_PORT}/world")
    return (json.loads(r.text), r.status_code)

def load_world():
    remote_world = fetch_world()[0]
    for remote_eid in remote_world:
        e = Entity(remote_eid)
        e_json = remote_world[remote_eid]
        e.realize(e_json)
        WORLD.append(e)

class Entity:
    def __init__(self, eid=None, name=None, pos=None, color=None, script=None, created_at= None, modified_at = None):
        self.modified_at = modified_at
        self.created_at = created_at
        self.script = script
        self.pos = pos
        self.name = name
        self.eid = eid

        self.body = None

    def fetch(self):
        r = requests.get(f"http://{HOST_NAME}:{HOST_PORT}/{self.eid}")
        return (json.loads(r.text), r.status_code)

    def realize(self, entity_json):
        self.eid = entity_json["id"]
        self.script = entity_json["script"]
        self.pos = entity_json["pos"]
        #self.color = entity_json["color"]
        self.name = entity_json["name"]
        self.created_at = entity_json["created_at"]
        self.modified_at = entity_json["modified_at"]
        for k in DEFAULT_PROPERTIES_ON_CREATE:
            if not k in entity_json:
                entity_json[k] = DEFAULT_PROPERTIES_ON_CREATE[k]
        shapes = {'box':vpython.box, 'sphere':vpython.sphere}
        print(f"radius: {entity_json['radius']}")
        self.body = shapes[entity_json['shape']](pos = vpython.vec(*self.pos),
                                                 size = vpython.vec(*entity_json['size']),
                                                 axis = vpython.vec(*entity_json['axis']),
                                                 color = vpython.vec(*entity_json['color']),
                                                 radisu = entity_json['radius'])
        print(self.body.__dict__)

print("fetching world...")
load_world()
print("world model realized.")