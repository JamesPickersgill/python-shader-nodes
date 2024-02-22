from typing import Dict

from shader_nodes import VectorSocket
from ._base_node import _BaseNode


class TextureCoordinate(_BaseNode):
    def blender_method(self, node_tree, object=None, from_instancer: bool = False) -> Dict[str, VectorSocket]:
        node = node_tree.nodes.new(type="ShaderNodeTexCoord")
        return {
            'Generated': VectorSocket(node.outputs[0]),
            'Normal': VectorSocket(node.outputs[1]),
            'UV': VectorSocket(node.outputs[2]),
            'Object': VectorSocket(node.outputs[3]),
            'Camera': VectorSocket(node.outputs[4]),
            'Window': VectorSocket(node.outputs[5]),
            'Reflection': VectorSocket(node.outputs[6])
        }

    def python_method(self):
        raise Exception('Not Implemented')


textureCoordinate = TextureCoordinate()
