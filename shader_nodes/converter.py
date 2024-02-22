from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, get_type_hints, Callable, Any, Tuple
import bpy

import inspect
from abc import ABC, abstractmethod
from shader_nodes import ColourSocket, FloatSocket, Socket, add, current_node_tree, auto_position


# todo: deal with node.location, maybe see if auto positioning exists
# todo: allow non-socket arguments, i.e. colour step input for colour ramp
def nodegroup(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        params = inspect.signature(func).parameters
        args_kwargs = dict(zip(params.keys(), args))
        all_kwargs = {**args_kwargs, **kwargs}

        # for node_group in bpy.data.node_groups:
        #     if node_group.name == func.__name__:
        #         # todo: create new instance before return
        #         return node_group.outputs

        # todo: increment the name if the non-socket arguemnts differ
        node_tree = bpy.data.node_groups.new(func.__name__, 'ShaderNodeTree')
        node_tree_inputs = node_tree.nodes.new('NodeGroupInput')
        node_tree_outputs = node_tree.nodes.new('NodeGroupOutput')

        hints = get_type_hints(func)

        return_types = hints.pop('return')
        if not hasattr(return_types, '__iter__'):
            return_types = [return_types]
        for return_type in return_types:
            node_tree.interface.new_socket(socket_type=return_type.blender_name, name=return_type.default_name,
                                           in_out='OUTPUT')

        new_kwargs = dict()
        for idx, (name, socket_type) in enumerate(hints.items()):
            node_tree.interface.new_socket(socket_type=socket_type.blender_name, name=name, in_out='INPUT')
            # todo: wrap this properly
            new_kwargs[name] = FloatSocket(node_tree_inputs.outputs[idx])

        # Set node tree context
        outer_node_tree = current_node_tree.get()
        token = current_node_tree.set(node_tree)

        try:
            # run function to generate tree
            func_outputs = func(**new_kwargs)

            for func_output, tree_output in zip(func_outputs, node_tree_outputs.inputs):
                # todo: asset these are the same types, and there are the same number
                node_tree.links.new(func_output.socket, tree_output)

            auto_position(node_tree)
        finally:
            # reset context
            current_node_tree.reset(token)
            current_node_tree.set(outer_node_tree)

        if outer_node_tree is not None:
            # instance the node group
            outer_group_node = outer_node_tree.nodes.new('ShaderNodeGroup')
            outer_group_node.node_tree = node_tree

            for name, value in all_kwargs.items():
                outer_node_tree.links.new(value.socket, outer_group_node.inputs[name])

            # todo: wrap these correctly
            return [FloatSocket(socket) for socket in outer_group_node.outputs]
        raise
    return wrapper


def material(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        material = bpy.data.materials.new(name="CustomMaterial")
        material.use_nodes = True
        node_tree = material.node_tree
        node_tree.nodes.clear()

        # Set node tree context
        token = current_node_tree.set(node_tree)

        try:
            func_output = func(*args, **kwargs)

            if hasattr(func_output, '__iter__'):
                assert len(func_output) == 1, f'Can onlt pass one socket to material output. {len(func_output)} sockets were passed.'
                func_output = func_output[0]
            material_output = node_tree.nodes.new(type='ShaderNodeOutputMaterial')
            node_tree.links.new(func_output.socket, material_output.inputs['Surface'])
            auto_position(node_tree)
        finally:
            current_node_tree.reset(token)

        return material

    return wrapper



