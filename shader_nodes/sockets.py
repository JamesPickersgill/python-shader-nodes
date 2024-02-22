class _Socket:
    def __init__(self, socket):
        self.socket = socket

    def __add__(self, other):
        from shader_nodes.nodes import add
        return add(self, other)

    def __mul__(self, other):
        from shader_nodes.nodes import multiply
        return multiply(self, other)

    def __pow__(self, _power, modulo=None):
        from shader_nodes.nodes import power
        return power(self, _power)

    def __sub__(self, other):
        from shader_nodes.nodes import subtract
        return subtract(self, other)


class ColourSocket(_Socket):
    blender_name = 'NodeSocketColor'
    default_name = 'Colour'


class FloatSocket(_Socket):
    blender_name = 'NodeSocketFloat'
    default_name = 'Float'


class VectorSocket(_Socket):
    blender_name = 'NodeSocketVector'
    default_name = 'Vector'


class ShaderSocket(_Socket):
    blender_name = 'NodeSocketShader'
    default_name = 'Shader'


Socket = ColourSocket | FloatSocket | VectorSocket | ShaderSocket
