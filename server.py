import datetime

from bottle import route, run, request, response, debug, default_app
import uuid, json
from threecommon import *

box_uuid = "69c7e584-0907-4dad-9c6f-12550fb69445"

WORLD = {
    box_uuid:{
        "name":"box1",
        "shape":"sphere",
        "pos":(0, 0, 0),
        "script":None,
        "id": box_uuid,
        "created_at":datetime.datetime.now().isoformat(),
        "modified_at":datetime.datetime.now().isoformat()
     }
}

SCRIPTS = {}
STARTUP = datetime.datetime.now()



def is_float(n):
    try:
        float(n)
        return True
    except:
        return False

@route("/")
def index():
    return f"""<title>3d-over-http</title>
    you've reached the 3d-over-http test server<br>
    try the route <code>/world</code> in your browser<br>
    last restarted at {STARTUP.isoformat()}<br>
    hosting {len(WORLD)} entities and {len(SCRIPTS)} scripts"""

@route("/world", method="GET")
@route("/world/", method="GET")
def get_world():
    return WORLD

@route("/world", method="POST")
@route("/world/", method="POST")
def create_entity():
    try:
        object = json.loads(request.POST.object)
    except:
        response.status = 400
        return "post request must supply key object with value that is valid JSON"


    if not all([prop in object for prop in REQUIRED_PROPERTIES_ON_CREATE]):
        response.status = 400
        return f"objects must have properties {REQUIRED_PROPERTIES_ON_CREATE}"
    if not object['shape'] in VALID_SHAPES:
        response.status = 400
        return f"shape must be one of {VALID_SHAPES}"
    if not len(object['pos']) == 3 or not all(is_float(e) for e in object['pos']):
        response.status = 400
        return "pos must be a tuple of three floats"

    global WORLD
    new_id = str(uuid.uuid4())
    new_object = {}
    for prop in FILLABLE_PROPERTIES_ON_CREATE:
        if prop in object: new_object[prop] = object[prop]
    for prop in NULLABLE_PROPERTIES_ON_CREATE:
        if not prop in new_object:
            object[prop] = None
    new_object["id"] = new_id
    WORLD[new_id] = new_object
    return new_id


@route("/world/<eid>", method="GET")
@route("/world/<eid>/", method="GET")
def get_entity(eid):
    try:
        return WORLD[eid]
    except KeyError:
        response.status = 404
        return f"no object with id {eid}"

@route("/world/<eid>", method="PATCH")
@route("/world/<eid>/", method="PATCH")
def patch_entity(eid):
    try:
        entity = WORLD[eid]
    except KeyError:
        response.status = 404
        return f"no object with id {eid}"

    try:
        updates = json.loads(request.POST.updates)
    except:
        response.status = 400
        return "patch request must supply updates object with value that is valid JSON"

    updated = 0
    for prop in updates:
        print(f"checking update property {prop}")
        if prop in READONLY_PROPERTIES:
            response.status = 400
            return f"{prop} is readonly"
        elif not prop in entity:
            return f"{prop} is not a valid property"
        elif prop == 'pos':
            if not len(updates[prop]) == 3 or not all(is_float(e) for e in updates[prop]):
                response.status = 400
                return "pos must be a tuple of three floats"
        #return json.dumps(updates)
        entity[prop] = updates[prop]
        updated += 1

    entity['modified_at'] = datetime.datetime.now().isoformat()
    return f"updated {updated} properties"







application = default_app()
debug(True)
if __name__ == "__main__":
	print("[INFO] Starting server")
	run(app=application, host="localhost", port=80,
		debug=True)
else:
	print("[INFO] Not in __main__, continuing with default_app only instantiated")

