import bpy
import os
from PIL import Image
from src.environment import Environment

class BlendEnvironment(Environment):
    """Link between environment and blender"""

    def __init__(self):
        pass

    def create_terrain(self, image_path):
        image_dir, image_name = os.path.split(image_path)
        image = os.path.splitext(image_name)[0]
        
        i = Image.open(image_path)
        maxi = max(i.size[0], i.size[1])
        i.close()
        
        bpy.ops.object.delete(use_global=False)
        # maybe we need to activate import_image.to_plane within blender...
        bpy.ops.import_image.to_plane(files=[{"name":image_name}], directory=image_dir, filter_image=True, filter_movie=True, filter_glob="", relative=False)
        bpy.ops.transform.resize(value=(14, 14, 14), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.subdivide(number_cuts=maxi, smoothness=0)
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.modifier_add(type='DISPLACE')
        bpy.context.object.modifiers["Displace"].texture = bpy.data.textures[image]
        bpy.context.object.modifiers["Displace"].strength = 0.2
        bpy.context.object.modifiers["Displace"].texture_coords = 'UV'
        bpy.ops.object.modifier_add(type='SUBSURF')
        bpy.data.lamps['Lamp'].type = 'SUN'
        bpy.context.scene.render.engine = 'CYCLES'


    def render(self, final_result):
        bpy.context.scene.render.filepath = final_result
        bpy.context.scene.render.resolution_x = 1920
        bpy.context.scene.render.resolution_y = 1080
        bpy.ops.render.render(write_still=True)


# if __name__ == "__main__":
#     l = BlendEnvironment()
#     l.create_terrain("/home/raphael/ensl/2a/pi/tests/mt-ruapehu-and-mt-ngauruhoe.png")
#     l.render("/tmp/bli.png")
