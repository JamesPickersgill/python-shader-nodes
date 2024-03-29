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
