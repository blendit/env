import bpy
import random

# how to deal with this ? pencil.layers[0] = GP_Layer.001, ..., pencil.layers[n-1] = GP_Layer.00n, pencil.layers[n] = GP_Layer... (but GP Layer first one)
# nb, can change gen_name(i) in id ? maybe not...


def upd_enum(self, context):
    print(self['MyEnum'])


def initSceneProperties(scn):
    myItems = [('Vegetation', 'Vegetation', 'Vegetation'),
               ('Mountain', 'Mountain', 'Mountain'),
               ('Urban', 'Urban', 'Urban'),
               ('Water', 'Water', 'Water')]
    bpy.types.Scene.MyEnum = bpy.props.EnumProperty(
        items=myItems,
        name="Feature choice",
        update=upd_enum)
    scn['MyEnum'] = 2
    scn["i"] = 0
    return


def print_points():
    # print points defined using pencil
    for i, pencil in enumerate(bpy.data.grease_pencil[0].layers):
        print("step " + str(i))
        try:
            for stroke in enumerate(pencil.active_frame.strokes):
                stroke_points = pencil.active_frame.strokes[0].points
                for point in stroke_points:
                    print("\t(" + str(point.co.x) + ", " + str(point.co.y) + ", " + str(point.co.z) + ")")
        except AttributeError:
            print("\tempty")
            

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
        layout.operator("drawenv.execute")
        layout.operator("drawenv.stop")
        layout.operator("drawenv.print")


class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "drawenv.execute"
    bl_label = "Draw something"

    def execute(self, context):
        self.report({'INFO'}, "starting drawing")
        bpy.ops.view3d.viewnumpad(type='TOP', align_active=False)
        bpy.ops.gpencil.draw('INVOKE_REGION_WIN', mode="DRAW_POLY")
        change_color(bpy.context.scene["i"])
        return {'FINISHED'}


class OBJECT_OT2_ToolsButton(bpy.types.Operator):
    bl_idname = "drawenv.stop"
    bl_label = "Done"

    def execute(self, context):
        bpy.context.scene["i"] += 1
        bpy.ops.gpencil.layer_add()
        bpy.ops.gpencil.layer_move()
        self.report({'INFO'}, "stopping drawing")
        return {'FINISHED'}


class OBJECT_OT3_ToolsButton(bpy.types.Operator):
    bl_idname = "drawenv.print"
    bl_label = "Print points"

    def execute(self, context):
        print_points()
        return {'FINISHED'}

    
class FeaturePanel(bpy.types.Panel):
    bl_category = "ENV"
    bl_label = "feature panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        layout.prop(scn, 'MyEnum')


initSceneProperties(bpy.context.scene)
bpy.utils.register_module(__name__)
