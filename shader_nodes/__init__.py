import contextvars

current_node_tree = contextvars.ContextVar('current_node_tree')

from .auto_position import auto_position
from .sockets import ColourSocket, VectorSocket, FloatSocket, ShaderSocket, Socket
from .converter import material, nodegroup
