# Shortcut : blender -P interface.py
bl_info = {
    "name": "Environment plug-in",
    "category": "Object",
}

import bpy
import os
import sys

script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(script_dir)
print(script_dir)

from src.blend_environment import BlendEnvironment


def initSceneProperties(scn):
    bpy.types.Scene.res = bpy.props.IntProperty(name="Resolution", default=1, min=1, max=100)
    scn["res"] = 1
    bpy.types.Scene.path = bpy.props.StringProperty(
        name="",
        description="Path to Directory",
        default="",
        maxlen=1024,
        subtype='FILE_PATH')
    scn["path"] = ""
    return

initSceneProperties(bpy.context.scene)


class Run_button(bpy.types.Panel):
    bl_label = "Environment panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    def draw(self, context):
        layout = self.layout
        scn = context.scene
        layout.prop(scn, 'res')
        layout.prop(scn, 'path')
        layout.operator("env.interface")


class EnvInterface(bpy.types.Operator):
    """Environment plug-in"""
    bl_idname = "env.interface"
    bl_label = "Run import"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scn = bpy.context.scene
        self.report({'INFO'}, "env.interface :\n  Resolution : %d\n  Path : %s" % (scn["res"], scn["path"]))
        a = BlendEnvironment()
        a.create_terrain(scn["path"])
        return {'FINISHED'}


# def menu_func(self, context):
#     self.layout.operator(EnvInterface.bl_idname)

# # store keymaps here to access after registration
# addon_keymaps = []


def register():
    bpy.utils.register_module(__name__)
#     bpy.types.VIEW3D_MT_object.append(menu_func)

#     # handle the keymap
#     wm = bpy.context.window_manager
#     km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
#     kmi = km.keymap_items.new(EnvInterface.bl_idname, 'SPACE', 'PRESS', ctrl=True, shift=True)
#     kmi.properties.total = 4
#     addon_keymaps.append((km, kmi))


def unregister():
    bpy.utils.unregister_module(__name__)
#     bpy.types.VIEW3D_MT_object.remove(menu_func)

#     # handle the keymap
#     for km, kmi in addon_keymaps:
#         km.keymap_items.remove(kmi)
#     addon_keymaps.clear()


if __name__ == "__main__":
    register()
