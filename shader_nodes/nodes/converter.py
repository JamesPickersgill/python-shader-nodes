from typing import Optional, Tuple

import numpy as np

from shader_nodes import FloatSocket, ColourSocket, VectorSocket, Socket
from ._base_node import _BaseNode


class SeparateColour(_BaseNode):
    def blender_method(self, node_tree, colour: Optional[ColourSocket]) -> Tuple[FloatSocket, FloatSocket, FloatSocket]:
        node = node_tree.nodes.new(type="ShaderNodeSeparateColor")
        if colour:
            node_tree.links.new(colour.socket, node.inputs[0])
        outputs = (FloatSocket(socket=node.outputs[0]),
                   FloatSocket(socket=node.outputs[1]),
                   FloatSocket(socket=node.outputs[2]))
        return outputs

    def python_method(self, colour):
        return colour[:, :, 0], colour[:, :, 1], colour[:, :, 2]


class SeparateXYZ(_BaseNode):
    def blender_method(self, node_tree, vector: Optional[VectorSocket]) -> Tuple[FloatSocket, FloatSocket, FloatSocket]:
        node = node_tree.nodes.new(type="ShaderNodeSeparateXYZ")
        if vector:
            node_tree.links.new(vector.socket, node.inputs[0])
        outputs = (FloatSocket(socket=node.outputs[0]),
                   FloatSocket(socket=node.outputs[1]),
                   FloatSocket(socket=node.outputs[2]))
        return outputs

    def python_method(self, vector):
        return vector[:, :, 0], vector[:, :, 1], vector[:, :, 2]


class CombineXYZ(_BaseNode):
    def blender_method(self, node_tree, x: Optional[FloatSocket], y: Optional[FloatSocket], z: Optional[FloatSocket]) \
            -> VectorSocket:
        node = node_tree.nodes.new(type="ShaderNodeCombineXYZ")

        if isinstance(x, Socket):
            node_tree.links.new(x.socket, node.inputs[0])
        else:
            node.inputs[0].default_value = x

        if isinstance(y, Socket):
            node_tree.links.new(y.socket, node.inputs[1])
        else:
            node.inputs[1].default_value = y

        if isinstance(z, Socket):
            node_tree.links.new(z.socket, node.inputs[2])
        else:
            node.inputs[2].default_value = z

        return VectorSocket(node.outputs[0])

    def python_method(self, x, y, z):
        # todo: test this, not sure it will work for most cases
        return np.stack([x, y, z])


separateColour = SeparateColour()
separateXYZ = SeparateXYZ()
combineXYZ = CombineXYZ()
