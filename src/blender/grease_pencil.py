import bpy
import random

i = 0  # global variable is baaad. Improvement : add it in the context...


def print_points():
    # print points defined using pencil
    pencil = bpy.data.grease_pencil[0]
    for i, stroke in enumerate(pencil.layers[0].active_frame.strokes):
        print("step " + str(i))
        stroke_points = pencil.layers[0].active_frame.strokes[i].points
        for point in stroke_points:
            print((point.co.x, point.co.y, point.co.z))
            

def gen_name(i):
    if(i == 0):
        name = "GP_Layer"
    else:
        name = "GP_Layer." + "{0:0=3d}".format(i)
    return name


def change_color(i):
    name = gen_name(i)
    bpy.data.grease_pencil["GPencil"].layers[name].fill_color = (random.random(), random.random(), random.random())
    print("colors " + str(bpy.data.grease_pencil["GPencil"].layers[name].fill_color[0]) +
          " " + str(bpy.data.grease_pencil["GPencil"].layers[name].fill_color[1]) +
          " " + str(bpy.data.grease_pencil["GPencil"].layers[name].fill_color[2]))
    bpy.data.grease_pencil["GPencil"].layers[name].fill_alpha = 1


class ToolsPanel(bpy.types.Panel):
    bl_category = "ENV"
    bl_label = "env panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        layout.operator("path.execute")
        layout.operator("path.stop")


class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "path.execute"
    bl_label = "Draw me something"

    def execute(self, context):
        global i
        self.report({'INFO'}, "starting drawing")
        bpy.ops.gpencil.draw('INVOKE_REGION_WIN', mode="DRAW_POLY")
        change_color(i)
        return {'FINISHED'}


class OBJECT_OT2_ToolsButton(bpy.types.Operator):
    bl_idname = "path.stop"
    bl_label = "Done"

    def execute(self, context):
        global i
        i += 1
        bpy.ops.gpencil.layer_add()
        bpy.ops.gpencil.layer_move()
        self.report({'INFO'}, "stopping drawing")
        return {'FINISHED'}
    

bpy.utils.register_module(__name__)
    
# change_color()
# print_points()
