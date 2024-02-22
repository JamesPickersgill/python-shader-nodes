# python-shader-nodes
Helpers to make creating blender shader nodes in python more developer friendly.

**This project is in a proof of concept phase, so many features are missing**. 
Happy to add things if people find this tool useful.


## What is this?
Creating shader node materials with blender's python API is a bit annoying. To simply multiply you'd need all this 
```python
node_group = bpy.data.node_groups.new('Group Name', 'ShaderNodeTree')
multiply_r = node_group.nodes.new(type="ShaderNodeMath")
multiply_r.operation = 'MULTIPLY'
multiply_r.inputs[1].default_value = 0.299
multiply_r.location = (-300, 100)
node_group.links.new(separate_rgb.outputs['R'], multiply_r.inputs[0])
node_group.links.new(multiply_r.outputs[0], add_rg.inputs[0])
```

With python shader nodes this becomes

```python
from shader_nodes import material, nodegroup, ColourSocket, FloatSocket

@nodegroup
def multiply_r(input_value: FloatSocket, multiply_by: float) -> FloatSocket:
    return input_value * multiply_by
```

Far more pythonic!

## Gradient Example

The following code generates this node tree,

![Kaleidoscope example nodetree](https://github.com/JamesPickersgill/python-shader-nodes/blob/master/examples/kaleidoscope%20nodes.jpg)

which produces this image:

![Kaleidoscope example output](https://github.com/JamesPickersgill/python-shader-nodes/blob/master/examples/kaleidoscope%20output.jpg)


```python
import math
from shader_nodes import material, nodegroup, ColourSocket, FloatSocket
from shader_nodes.nodes import arctan2, textureCoordinate, separateXYZ, pingpong, sin, cos, combineXYZ, imageTexture
import bpy


@nodegroup
def euler_to_polar(x: FloatSocket, y: FloatSocket) -> [FloatSocket, FloatSocket]:
    r = (x ** 2 + y ** 2) ** 0.5
    theta = arctan2(y, x)
    return r, theta


@nodegroup
def polar_to_euler(r: FloatSocket, theta: FloatSocket) -> [FloatSocket, FloatSocket]:
    x = r * cos(theta)
    y = r * sin(theta)
    return x, y


@material
def kaleidoscope_material(image_path: str, segments: int) -> ColourSocket:
    coordinates = textureCoordinate()['Object']
    x, y, _ = separateXYZ(coordinates)
    r, theta = euler_to_polar(x, y)
    r -= 3  # to move image to nicer demo location
    theta = pingpong(theta, math.pi / (2 * segments))
    x, y = polar_to_euler(r, theta)
    new_coordinates = combineXYZ(x, y, 1.0)
    image = imageTexture(new_coordinates, image_path=image_path)
    return image['Colour']


if __name__ == '__main__':
    material = kaleidoscope_material(image_path='dog.jpg', segments=3)
    bpy.ops.mesh.primitive_plane_add()
    plane = bpy.context.object
    bpy.ops.object.material_slot_add()
    plane.material_slots[0].material = material
    bpy.ops.wm.save_as_mainfile(filepath='example.blend')

```

## Installation
1. Clone the repo with `gh repo clone JamesPickersgill/python-shader-nodes`
2. pip install the shader_nodes module, i.e. `pip install ~/python-shader-nodes/shader-nodes`


## Planned Features
- Calling shader-node functions as regular python functions for testing
- Implementing all blender shader nodes
