import bpy
import os
import sys
import subprocess
import ast
import random

script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(script_dir)

# Get system's python path
proc = subprocess.Popen('python3 -c "import sys; print(sys.path)"', stdout=subprocess.PIPE, shell=True)
out, err = proc.communicate()
paths = ast.literal_eval(out.decode("utf-8"))
sys.path += (paths)

from shapely.geometry import Polygon
from shapely.affinity import translate

from src.blender.blend_environment import BlendEnvironment
from src.environment import Environment
from src.landscape import Mountain, MountainImg, Vegetation
from src.model import AbstractModel

# how to deal with this ? pencil.layers[0] = GP_Layer.001, ..., pencil.layers[n-1] = GP_Layer.00n, pencil.layers[n] = GP_Layer... (but GP Layer first one)
# nb, can change gen_name(i) in id ? maybe not...

feature_list = []
# if we put feature_list into scn, it is transformed into a read-only IDPropertyArray :'(


def upd_enum(self, context):
    print(self['MyEnum'])


def initSceneProperties(scn):
    myItems = [('Mountain', 'Mountain', 'Mountain'),
               ('MountainImg', 'MountainImg', 'MountainImg'),
               ('Vegetation', 'Vegetation', 'Vegetation'),
               ('Urban', 'Urban', 'Urban'),
               ('Water', 'Water', 'Water')]
    bpy.types.Scene.MyEnum = bpy.props.EnumProperty(
        items=myItems,
        name="Feature choice",
        update=upd_enum)
    scn["myItems"] = myItems
    scn['MyEnum'] = 0
    scn["i"] = 0
    scn["models_scale"] = 1
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


def dist(a, b):
    return (a[0] - b[0])**2 + (a[1] - b[1])**2


def gen_feature(feature_name, shape, transl, scaling):
    print("Called gen_feature @ %s" % feature_name)
    # let's first translate our feature.
    ip = Polygon(list(shape))  # map(lambda x: (x[0], 4x[1]), shape)))
    p = translate(ip, xoff=transl[0], yoff=transl[1])
    if(feature_name == "Mountain"):
        center_z = 0
        center_pos = p.centroid.coords[0]
        rd = int((max([dist(x, center_pos) for x in p.exterior.coords]) / 2) ** 0.5)
        print("Radius = %d" % rd)
        print("Center = %d, %d" % (center_pos[0], center_pos[1]))
        return Mountain(rd, center_z, center_pos)
    elif(feature_name == "MountainImg"):
        center_z = 0
        center_pos = p.bounds[0:2]
        print("Center = %d, %d" % (center_pos[0], center_pos[1]))
        return MountainImg(p, center=center_pos)
    elif(feature_name == "Roads"):
        pass
    elif(feature_name == "Vegetation"):
        for a in p.exterior.coords:
            print(a)
        return Vegetation(p, model=AbstractModel("../../models/vegetation/pine_tree/Pine_4m.obj", 0.01, (0, 0)), tree_number=50)
    elif(feature_name == "Urban"):
        pass
    elif(feature_name == "WaterArea"):
        pass
    elif(feature_name == "River"):
        pass


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
        layout.operator("drawenv.gen")
        layout.operator("drawenv.print")
        layout.operator("drawenv.hide")


class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "drawenv.execute"
    bl_label = "Draw something"

    def execute(self, context):
        self.report({'INFO'}, "starting drawing")
        bpy.ops.view3d.viewnumpad(type='TOP', align_active=False)
        bpy.ops.gpencil.draw('INVOKE_REGION_WIN', mode="DRAW_POLY")
        change_color(context.scene["i"])
        return {'FINISHED'}


class OBJECT_OT2_ToolsButton(bpy.types.Operator):
    bl_idname = "drawenv.stop"
    bl_label = "Done"

    def execute(self, context):
        scn = context.scene
        self.report({'INFO'}, "stopping drawing")
        # We add this new feature
        # We should translate everything, here or when exporting the env
        # Idea : find bounding box, and translate 2 times...
        # shape_2d = [(p.co.x, p.co.y) for p in bpy.data.grease_pencil[0].layers[scn["i"]].active_frame.strokes[0].points]
        # feature_list.append(gen_feature(scn["myItems"][scn["MyEnum"]][0], shape_2d))
        feature_list.append(scn["myItems"][scn["MyEnum"]][0])
        scn["i"] += 1
        bpy.ops.gpencil.layer_add()
        return {'FINISHED'}


class OBJECT_OT3_ToolsButton(bpy.types.Operator):
    bl_idname = "drawenv.print"
    bl_label = "Print points"

    def execute(self, context):
        print_points()
        return {'FINISHED'}

    
class OBJECT_OT4_ToolsButton(bpy.types.Operator):
    bl_idname = "drawenv.hide"
    bl_label = "Hide/unhide gpencil"

    def execute(self, context):
        scn = context.scene
        for i in range(scn["i"]):
            bpy.data.grease_pencil[0].layers[i].hide = not bpy.data.grease_pencil["GPencil"].layers[i].hide
        return {'FINISHED'}


class OBJECT_OT4_ToolsButton(bpy.types.Operator):
    bl_idname = "drawenv.gen"
    bl_label = "Generate environment"

    def execute(self, context):
        scn = context.scene
        bpy.ops.view3d.viewnumpad(type='CAMERA', align_active=False)
        #scaling = max(bb[2] - bb[0], max(bb[2] - bb[0], bb[3] - bb[1])bb[3] - bb[1]) / 28
        scaling = 5
        shapes = [[(scaling * p.co.x, - scaling * p.co.y) for p in bpy.data.grease_pencil[0].layers[i].active_frame.strokes[0].points] for i in range(scn["i"])]
        bb = bounds(shapes[0])
        for shape in shapes[1:]:
            s = bounds(shape)
            bb = (min(bb[0], s[0]), min(bb[1], s[1]), max(bb[2], s[2]), max(bb[3], s[3]))
        print("Res x %d; res y %d" % ((bb[2] - bb[0]), (bb[3] - bb[1])))
        my_features = [gen_feature(feature_list[i], shapes[i], (-bb[0], -bb[1]), scaling) for i in range(len(shapes))]
        env = Environment(my_features, x=1 + int(bb[2] - bb[0]), y=1 + int(bb[3] - bb[1]))
        benv = BlendEnvironment(resize=max(bb[2] - bb[0], bb[3] - bb[1]) // (2*scaling), translation=False)
        # scn["models_scale"] = 1 / (max(bb[2] - bb[0], bb[3] - bb[1]) // (2*scaling))
        benv.export_img(env, 2)
        return {'FINISHED'}


def bounds(point_list):
    min_x, min_y = point_list[0]
    max_x, max_y = point_list[0]
    for p in point_list[1:]:
        min_x = min(min_x, p[0])
        max_x = max(max_x, p[0])
        min_y = min(min_y, p[1])
        max_y = max(max_y, p[1])
    return (min_x, min_y, max_x, max_y)
    

class FeaturePanel(bpy.types.Panel):
    bl_category = "ENV"
    bl_label = "feature panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        layout.prop(scn, 'MyEnum')


if __name__ == "__main__":
    initSceneProperties(bpy.context.scene)
    bpy.utils.register_module(__name__)
