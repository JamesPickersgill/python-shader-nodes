from typing import Optional, Callable
from shader_nodes import FloatSocket, Socket, VectorSocket, ColourSocket, ShaderSocket
from numbers import Real
from ._base_node import _BaseNode
import numpy as np


class MathsNode(_BaseNode):
    def __init__(self, operation: str,
                 vector_operation: Optional[str],
                 colour_operation: Optional[str],
                 python_function: Callable):
        self.operation = operation
        self.vector_operation = vector_operation
        self.colour_operation = colour_operation
        self.python_function = python_function

    def blender_method(self, node_tree, input1: Socket | Real = 0.0, input2: Socket | Real = 0.0) -> Socket:
        if isinstance(input1, ShaderSocket) or isinstance(input2, ShaderSocket):
            assert self.operation == 'ADD', f'Can only add shader sockets, not {self.operation.lower()} them.'
            node = node_tree.nodes.new(type="ShaderNodeAddShader")
            output_type = ShaderSocket
        elif isinstance(input1, VectorSocket) or isinstance(input2, VectorSocket):
            assert self.vector_operation is not None, f'Can\'t use operation "{self.operation}" with vector inputs'
            node = node_tree.nodes.new(type="ShaderNodeVectorMath")
            node.operation = self.vector_operation
            output_type = VectorSocket
        elif isinstance(input1, ColourSocket) or isinstance(input2, VectorSocket):
            if self.colour_operation is not None:
                node = node_tree.nodes.new(type='ShaderNodeMixRGB')
                node.operation = self.colour_operation
                output_type = ColourSocket
            else:
                # fallback to using vector math is colour mix is not defined
                assert self.vector_operation is not None, f'Can\'t use operation "{self.operation}" with vector inputs'
                node = node_tree.nodes.new(type="ShaderNodeVectorMath")
                node.operation = self.vector_operation
                output_type = VectorSocket
        else:
            node = node_tree.nodes.new(type="ShaderNodeMath")
            node.operation = self.operation
            output_type = FloatSocket

        if isinstance(input1, Socket):
            node_tree.links.new(input1.socket, node.inputs[0])
        else:
            node.inputs[0].default_value = input1

        if isinstance(input2, Socket):
            node_tree.links.new(input2.socket, node.inputs[1])
        else:
            node.inputs[1].default_value = input2

        return output_type(socket=node.outputs[0])

    def python_method(self, input1, input2):
        return self.python_function(input1, input2)


# TODO: 'DIVIDE', 'LOGARITHM', 'SQRT', 'INVERSE_SQRT', 'ABSOLUTE',
# 'EXPONENT', 'MINIMUM', 'MAXIMUM', 'LESS_THAN', 'GREATER_THAN', 'SIGN', 'COMPARE', 'SMOOTH_MIN', 'SMOOTH_MAX',
# 'ROUND', 'FLOOR', 'CEIL', 'TRUNC', 'FRACT', 'MODULO', 'FLOORED_MODULO', 'WRAP', 'SNAP', 'SINE', 'COSINE',
# 'TANGENT', 'ARCSINE', 'ARCCOSINE', 'ARCTANGENT', 'SINH', 'COSH', 'TANH', 'RADIANS', 'DEGREES'
add = MathsNode('ADD', 'ADD', 'ADD', lambda x, y: x + y)
subtract = MathsNode('SUBTRACT', 'SUBTRACT', 'SUBTRACT', lambda x, y: x - y)
multiply = MathsNode('MULTIPLY', 'MULTIPLY', 'MULTIPLY', lambda x, y: x * y)
power = MathsNode('POWER', None, None, lambda x, y: x ** y)
arctan2 = MathsNode('ARCTAN2', None, None, np.arctan2)
pingpong = MathsNode('PINGPONG', None, None, None)
sin = MathsNode('SINE', 'SINE', None, np.sin)
cos = MathsNode('COSINE', 'COSINE', None, np.cos)
tan = MathsNode('TANGENT', 'TANGENT', None, np.cos)
