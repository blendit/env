import bpy
import os
import pickle
import time
from PIL import Image
from src.environment import Environment


class BlendEnvironment(Environment):
    """Link between environment and blender"""

    def __init__(self, pos, size):
        self.models = []
        (pos_x, pos_y) = pos
        (size_x, size_y) = size
        
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size_x = size_x
        self.size_y = size_y

    def create_terrain(self, image_path, res):
        image_dir, image_name = os.path.split(image_path)
        image = os.path.splitext(image_name)[0]
        
        i = Image.open(image_path)
        maxi = max(i.size[0], i.size[1])
        i.close()

        bpy.ops.object.delete(use_global=False)
        bpy.ops.mesh.primitive_plane_add(radius=0.5, view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))

        # Resize
        bpy.ops.transform.resize(value=(self.size_x / res, self.size_y / res, 20), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        
        t_x = - self.pos_x + self.size_x / 2
        t_y = self.pos_y - self.size_y / 2
        bpy.ops.transform.translate(value=(t_x, t_y, 0), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

        # Subdivide
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.subdivide(number_cuts=maxi, smoothness=0)
        for x in range(res - 1):
            bpy.ops.mesh.subdivide(smoothness=0)
        bpy.ops.transform.resize(value=(res, res, 1), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

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
            ob.modifiers["Displace"].mid_level = 0
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Displace")
            bpy.ops.object.modifier_add(type='SUBSURF')
            
        bpy.data.lamps['Lamp'].type = 'SUN'
        
    def import_env(self, pickle_path, res):
        f = open(pickle_path, 'rb')
        env = pickle.load(f)
        f.close()
        self.export_img(env, res)

    def export_img(self, env, res, scaling):
        image = "/tmp/env%s.png" % time.strftime("%d_%Hh%Mm%Ss")
        env.export_heightmap(image)
        self.create_terrain(image, res)

        # Import abstract models as reference objects
        amodel_dict = {}
        for amodel in env.abstract_models:
            bpy.ops.import_scene.obj(filepath=amodel.path, axis_forward='-Z', axis_up='Y')
            # Resize
            s = amodel.size * bpy.context.scene["models_scale"]
            bpy.ops.transform.resize(value=(s, s, s), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

            amodel_dict[amodel] = bpy.context.selected_objects

        # Duplicate reference objects
        for model in env.models:
            amodel = model.model

            # select model to duplicate
            bpy.ops.object.select_all(action='DESELECT')
            for o in amodel_dict[amodel]:
                o.select = True

            # duplicate
            x, y, z = model.pos3D
            x = x - self.pos_x
            y = - y + self.pos_y
            z = z * 10  / 255
            bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked": False, "mode": 'TRANSLATION'}, TRANSFORM_OT_translate={"value": (x / scaling, y / scaling, z), "constraint_axis": (False, False, False), "constraint_orientation": 'GLOBAL', "mirror": False, "proportional": 'DISABLED', "proportional_edit_falloff": 'SMOOTH', "proportional_size": 1, "snap": False, "snap_target": 'CLOSEST', "snap_point": (0, 0, 0), "snap_align": False, "snap_normal": (0, 0, 0), "gpencil_strokes": False, "texture_space": False, "remove_on_cancel": False, "release_confirm": False})

            self.models.append((amodel.size, bpy.context.selected_objects))

        # Delete reference objects
        bpy.ops.object.select_all(action='DESELECT')
        for amodel, objs in amodel_dict.items():
            for o in objs:
                o.select = True
        bpy.ops.object.delete()

    def render(self, final_result):
        bpy.context.scene.render.filepath = final_result
        bpy.context.scene.render.resolution_x = 1920
        bpy.context.scene.render.resolution_y = 1080
        bpy.context.scene.render.resolution_percentage = 100
        bpy.ops.render.render(write_still=True)
