import contextvars
current_node_tree = contextvars.ContextVar('current_node_tree')

from .auto_position import auto_position
from .sockets import ColourSocket, VectorSocket, FloatSocket, ShaderSocket, Socket
from .nodes import add, multiply, power, separateColour, arctan2, textureCoordinate, separateXYZ, pingpong, sin, cos, \
    tan, combineXYZ, voronoiTexture, imageTexture, subtract
from .converter import material, nodegroup

