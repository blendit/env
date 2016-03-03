# Shortcut : blender -P interface.py
# /home/raphael/ensl/2a/pi/blender-2.76b-linux-glibc211-x86_64/2.76/scripts/startup/bl_ui/properties_render.py
# addons/cycles/properties.py

bl_info = {
    "name": "Environment plug-in",
    "category": "Object",
}

import bpy

class Run_button(bpy.types.Panel):
    bl_label = "Environment panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    
    def draw(self, context):
        layout = self.layout
        layout.operator("object.pingpong", text="Ping")


class EnvInterface(bpy.types.Operator):
    """Environment plug-in"""
    bl_idname = "env.interface"
    bl_label = "Environment interface"
    bl_options = {'REGISTER', 'UNDO'}

    total = bpy.props.IntProperty(name="Resolution", default=1, min=1, max=100)
    test = bpy.props.BoolProperty(name="Run")
    path = bpy.props.StringProperty(
        name="",
        description="Path to Directory",
        default="",
        maxlen=1024,
        subtype='FILE_PATH')

#    layout.operator("hello.hello")

    def execute(self, context):
        self.report({'INFO'}, "env.interface :\n  Resolution : %d\n  Path : %s" % (self.total, self.path))
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(EnvInterface.bl_idname)

# store keymaps here to access after registration
addon_keymaps = []


def register():
    bpy.utils.register_class(EnvInterface)
    bpy.types.VIEW3D_MT_object.append(menu_func)

    # handle the keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
    kmi = km.keymap_items.new(EnvInterface.bl_idname, 'SPACE', 'PRESS', ctrl=True, shift=True)
    kmi.properties.total = 4
    addon_keymaps.append((km, kmi))


def unregister():
    bpy.utils.unregister_class(EnvInterface)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

    # handle the keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


if __name__ == "__main__":
    register()
