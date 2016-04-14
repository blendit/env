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
from src.feature import ImageFeature

# how to deal with this ? pencil.layers[0] = GP_Layer.001, ..., pencil.layers[n-1] = GP_Layer.00n, pencil.layers[n] = GP_Layer... (but GP Layer first one)
# nb, can change gen_name(i) in id ? maybe not...

feature_list = []
model_number_list = []
image_path_list = []
# if we put feature_list into scn, it is transformed into a read-only IDPropertyArray :'(
benv = BlendEnvironment((0, 0), (0, 0))
# could probably put this in context


def upd_enum(self, context):
    print(self['MyEnum'])


def update_scale(self, context):
    for (s, models) in benv.models:
        for model in models:
            model.scale[0] = s * context.scene.model_scaling
            model.scale[1] = s * context.scene.model_scaling
            model.scale[2] = s * context.scene.model_scaling


def initSceneProperties(scn):
    bpy.types.Scene.scaling = bpy.props.IntProperty(name="Scaling", default=1, min=1, max=10)
    scn["scaling"] = 1
    bpy.types.Scene.model_number = bpy.props.IntProperty(name="Number of models", default=20, min=1, max=400)
    scn["model_number"] = 20
    bpy.types.Scene.model_scaling = bpy.props.FloatProperty(name="Scaling of models", default=0.25, min=0, update=update_scale)
    scn["model_scaling"] = 0.25
    bpy.types.Scene.model_path = bpy.props.StringProperty(
        name="Path to models",
        description="Path to models",
        default="../../models/vegetation/Pine_4m.obj",
        maxlen=1024,
        subtype='FILE_PATH')
    scn["model_path"] = "../../models/vegetation/Pine_4m.obj"
    bpy.types.Scene.image_path = bpy.props.StringProperty(
        name="Patht to models",
        description="Path to models",
        default="../../hm.png",
        maxlen=1024,
        subtype='FILE_PATH')
    scn["image_path"] = "../../hm.png"
    myItems = [('MountainImg', 'MountainImg', 'MountainImg'),
               # ('Mountain', 'Mountain', 'Mountain'),
               ('Vegetation', 'Vegetation', 'Vegetation'),
               ('Image', 'Image', 'Image'),
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


def gen_feature(feature_name, model_number, image_path, shape, transl, scaling, scn):
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
    elif(feature_name == "Image"):
        f = ImageFeature(image_path)
        f.shape = p
        return f
    elif(feature_name == "Vegetation"):
        for a in p.exterior.coords:
            print(a)
        return Vegetation(p, model=AbstractModel(scn["model_path"], 0.02, (0, 0)), tree_number=model_number)
    elif(feature_name == "Urban"):
        pass
    elif(feature_name == "WaterArea"):
        pass
    elif(feature_name == "River"):
        pass


class ToolsPanel(bpy.types.Panel):
    bl_category = "Environment"
    bl_label = "Drawing panel"
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
        layout.prop(scn, "scaling")


class OBJECT_OT_ToolsButton(bpy.types.Operator):
    bl_idname = "drawenv.execute"
    bl_label = "Draw map"

    def execute(self, context):
        self.report({'INFO'}, "starting drawing")
        bpy.ops.view3d.viewnumpad(type='TOP')
        # bpy.ops.view3d.view_persportho()
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
        model_number_list.append(scn["model_number"])
        image_path_list.append(scn["image_path"])
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
    bl_label = "Hide/unhide blueprints"

    def execute(self, context):
        scn = context.scene
        for i in range(scn["i"]):
            bpy.data.grease_pencil[0].layers[i].hide = not bpy.data.grease_pencil["GPencil"].layers[i].hide
        return {'FINISHED'}


class OBJECT_OT4_ToolsButton(bpy.types.Operator):
    bl_idname = "drawenv.gen"
    bl_label = "Generate environment"

    def execute(self, context):
        global benv
        scn = context.scene
        # bpy.ops.view3d.viewnumpad(type='CAMERA', align_active=False)
        # scaling = max(bb[2] - bb[0], max(bb[2] - bb[0], bb[3] - bb[1])bb[3] - bb[1]) / 28
        scaling = scn["scaling"]
        shapes = [[] for i in range(scn["i"])]
        for i in range(scn["i"]):
            try:
                for p in bpy.data.grease_pencil[0].layers[i].active_frame.strokes[0].points:
                    shapes[i].append((scaling * p.co.x, - scaling * p.co.y))
            except AttributeError:
                pass
        bb = bounds(shapes[0])
        for shape in shapes[1:]:
            if(shape != []):
                s = bounds(shape)
                bb = (min(bb[0], s[0]), min(bb[1], s[1]), max(bb[2], s[2]), max(bb[3], s[3]))
        res_x = int(bb[2] - bb[0])
        res_y = int(bb[3] - bb[1])
        print("Res x %d; res y %d" % (res_x, res_y))
        
        my_features = [gen_feature(feature_list[i], model_number_list[i], image_path_list[i], shapes[i], (-bb[0], -bb[1]), scaling, scn) for i in range(len(shapes)) if shapes[i] != []]
        
        env = Environment(my_features, x=res_x, y=res_y)
        benv = BlendEnvironment((-bb[0], -bb[1]), (res_x, res_y))
        
        # scn["models_scale"] = 1 / (max(bb[2] - bb[0], bb[3] - bb[1]) // (2*scaling))
        benv.export_img(env, 2, scaling)
        for (s, models) in benv.models:
            for model in models:
                model.scale[0] = s * scn.model_scaling
                model.scale[1] = s * scn.model_scaling
                model.scale[2] = s * scn.model_scaling
        bpy.ops.object.editmode_toggle()
        bpy.ops.transform.resize(value=(1/scaling, 1/scaling, 1), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        bpy.ops.object.editmode_toggle()
        for i in range(scn["i"]):
            bpy.data.grease_pencil[0].layers[i].hide = not bpy.data.grease_pencil["GPencil"].layers[i].hide
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
    bl_category = "Environment"
    bl_label = "Feature choice"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        layout.prop(scn, 'MyEnum')


class EnvParamPanel(bpy.types.Panel):
    bl_category = "Environment"
    bl_label = "Vegetation parameters"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        layout.prop(scn, 'model_number')
        layout.prop(scn, 'model_scaling')
        layout.prop(scn, 'model_path')


class ImgParamPanel(bpy.types.Panel):
    bl_category = "Environment"
    bl_label = "Image parameters"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        layout.prop(scn, 'image_path')

        
if __name__ == "__main__":
    initSceneProperties(bpy.context.scene)
    bpy.utils.register_module(__name__)
