from abc import ABC, abstractmethod

from shader_nodes import current_node_tree


class _BaseNode(ABC):
    @abstractmethod
    def blender_method(self, *args, **kwargs):
        pass

    @abstractmethod
    def python_method(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        node_tree = current_node_tree.get()
        if node_tree:
            return self.blender_method(node_tree, *args, **kwargs)
        else:
            return self.python_method(*args, **kwargs)
