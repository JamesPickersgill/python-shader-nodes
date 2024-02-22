from typing import Dict, Optional

import bpy

from shader_nodes import FloatSocket, ColourSocket, VectorSocket, Socket
from ._base_node import _BaseNode


# todo: add input sockets to this
class VoronoiTexture(_BaseNode):
    def blender_method(self, node_tree) -> Dict[str, Socket]:
        node = node_tree.nodes.new(type="ShaderNodeTexVoronoi")
        return {
            'Distance': FloatSocket(node.outputs[0]),
            'Colour': ColourSocket(node.outputs[1]),
            'Position': VectorSocket(node.outputs[2]),
        }

    def python_method(self):
        raise Exception('Not Implemented')


class ImageTexture(_BaseNode):
    def blender_method(self, node_tree, vector: Optional[VectorSocket] = None, image_path: Optional[str] = None) -> \
    Dict[str, Socket]:
        node = node_tree.nodes.new(type="ShaderNodeTexImage")

        if image_path is not None:
            bpy.ops.image.open(filepath=image_path)
            image = bpy.data.images.get(image_path)
            node.image = image

        if vector is not None:
            node_tree.links.new(vector.socket, node.inputs[0])

        return {
            'Colour': ColourSocket(node.outputs[0]),
            'Alpha': FloatSocket(node.outputs[1]),
        }

    def python_method(self):
        raise Exception('Not Implemented')


voronoiTexture = VoronoiTexture()
imageTexture = ImageTexture()
