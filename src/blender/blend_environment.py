import bpy
import os
import pickle
import time
from PIL import Image
from src.environment import Environment


class BlendEnvironment(Environment):
    """Link between environment and blender"""

    def __init__(self, resize=14, translation=True):
        self.models = []
        self.resize = resize
        self.translation = translation

    def create_terrain(self, image_path, res):
        image_dir, image_name = os.path.split(image_path)
        image = os.path.splitext(image_name)[0]
        
        i = Image.open(image_path)
        maxi = max(i.size[0], i.size[1])
        i.close()

        bpy.ops.object.delete(use_global=False)
        bpy.ops.mesh.primitive_plane_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))

        if(self.translation):
            bpy.ops.transform.translate(value=(0, 0, 3.5), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        # Resize
        bpy.ops.transform.resize(value=(self.resize, self.resize, self.resize), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

        # Subdivide
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.subdivide(number_cuts=maxi, smoothness=0)
        for x in range(res - 1):
            bpy.ops.mesh.subdivide(smoothness=0)
        bpy.ops.object.editmode_toggle()
        
        # Add heightmap
        ob = bpy.context.object
        if ob is None or ob.type != 'MESH':
            print("Need an active Mesh object!")
        else:
            texture = bpy.data.textures.new(image, type='IMAGE')
            texture.image = bpy.data.images.load(image_path)
            
            bpy.ops.object.modifier_add(type='DISPLACE')
            ob.modifiers["Displace"].texture = bpy.data.textures[image]
            ob.modifiers["Displace"].strength = 0.5
            ob.modifiers["Displace"].texture_coords = 'UV'
            bpy.ops.object.modifier_add(type='SUBSURF')
        
        bpy.data.lamps['Lamp'].type = 'SUN'

    def import_env(self, pickle_path, res):
        f = open(pickle_path, 'rb')
        env = pickle.load(f)
        f.close()
        self.export_img(env, res)

    def export_img(self, env, res):
        image = "/tmp/env%s.png" % time.strftime("%d_%Hh%Mm%Ss")
        env.export_heightmap(image)
        self.create_terrain(image, res)

        # Import models
        for model in env.models:
            bpy.ops.import_scene.obj(filepath=model.model.path, axis_forward='-Z', axis_up='Y')
            
            self.models.append((model.model.size, bpy.context.selected_objects))

            s = model.model.size * bpy.context.scene["models_scale"]
            bpy.ops.transform.resize(value=(s, s, s), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
            bpy.ops.transform.translate(value=(-14, 14, 0), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

            x, y, z = model.pos3D
            x = x * 28 / env.res_x
            y = y * -28 / env.res_y
            z = z * 7 / 255
            bpy.ops.transform.translate(value=(x, y, z), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

    def render(self, final_result):
        bpy.context.scene.render.filepath = final_result
        bpy.context.scene.render.resolution_x = 1920
        bpy.context.scene.render.resolution_y = 1080
        bpy.context.scene.render.resolution_percentage = 100
        bpy.ops.render.render(write_still=True)
