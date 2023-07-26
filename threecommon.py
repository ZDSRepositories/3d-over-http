# Constants and methods common to client and server code.

REQUIRED_PROPERTIES_ON_CREATE = ['pos', 'shape']
NULLABLE_PROPERTIES_ON_CREATE = ['script']
FILLABLE_PROPERTIES_ON_CREATE = ['pos', 'shape', 'name', 'script']
DEFAULT_PROPERTIES_ON_CREATE = {'pos':(0,0,0), 'axis':(0,0,0), 'size':(1,1,1), 'color':(1,1,1), 'radius':0.5}
READONLY_PROPERTIES = ['id', 'shape', 'script', 'created_at', 'modified_at']
VALID_SHAPES = ['box', 'sphere']