import bpy
import os
import sys
import math
import glob



def Run():
    rootfolder = os.path.join(sys.argv[5])
    obj_extension = os.path.join(sys.argv[6])
    obj_name = os.path.join(sys.argv[7])
    output_path = os.path.join(sys.argv[8])
    studio_path = os.path.join(sys.argv[9])
    hdri_path = os.path.join(sys.argv[10])

    #Setup scene and render engine
    MyScene = bpy.context.scene
    MyScene.render.engine = 'CYCLES'
  
    Setup(MyScene, studio_path, hdri_path)
    Import(rootfolder, obj_extension)
    Place(MyScene)
    # Check(output_path, obj_name)
    Render(output_path, obj_name)
    Clean()

    # ArgTest()


def Setup(MyScene, studio_path, hdri_path):

    #Clean scene before render
    if "Cube" in MyScene.objects:
        bpy.data.objects["Cube"].select_set(True)
        bpy.ops.object.delete()

    if "Light" in MyScene.objects:
        bpy.data.objects["Light"].select_set(True)
        bpy.ops.object.delete()

    #Import studio
    bpy.ops.import_scene.obj(filepath = studio_path)


    #Lighting Setup
    MyScene.world.use_nodes = True
    world = MyScene.world
    NodeTree = bpy.data.worlds[world.name].node_tree
    EnvironmentNode = NodeTree.nodes.new(type='ShaderNodeTexEnvironment')
    backNode = NodeTree.nodes['Background']
    loaded_hdri=bpy.data.images.load(hdri_path)
    EnvironmentNode.image= loaded_hdri
    textureOut = EnvironmentNode.outputs['Color']
    backgroundIn = backNode.inputs['Color']
    NodeTree.links.new(textureOut, backgroundIn)
    backNode.inputs[1].default_value= 4

    #Camera setup
    def SetCamera(scene, c):
        pi = math.pi

        scene.camera.rotation_euler[0] = c[0] * (pi / 180.0)
        scene.camera.rotation_euler[1] = c[1] * (pi / 180.0)
        scene.camera.rotation_euler[2] = c[2] * (pi / 180.0)

        scene.camera.location.x = c[3]
        scene.camera.location.y = c[4]
        scene.camera.location.z = c[5]

        return
    
    config = list([66.9, 0, 28.9, 82.454, -1.47314, 1.2288])

    # Deselect everything in the scene so that we can delete only the camera
    bpy.ops.object.select_all(action="DESELECT")
    bpy.data.objects["Camera"].select_set(True)
    bpy.ops.object.delete()

    # Add a new camera with the setup values
    bpy.ops.object.camera_add()
    Camera = bpy.data.objects["Camera"]
    Camera.rotation_mode = "XYZ"

    MyScene.camera = Camera
    SetCamera(scene=MyScene, c=config)

    bpy.data.scenes["Scene"].cycles.use_denoising = True
    MyScene.render.resolution_x = 480
    MyScene.render.resolution_y= 270
    bpy.context.scene.render.resolution_percentage = 100

    Setup.default_fov = 35

def Import(rootfolder, obj_extension):
    candidate_object=rootfolder
    bpy.ops.import_scene.gltf(filepath=candidate_object, filter_glob="*.glb;*.gltf", import_pack_images=True)

def Place(MyScene):
    myobject=None
    # Check whether there are one or several objects, and unite all
    Objects_in_scene = []
    for object in MyScene.objects:
        if object.type == "MESH" and object.name != "Decor_Plane":
            bpy.data.objects[object.name].select_set(True)
            Objects_in_scene.append(object)
        if len(Objects_in_scene)>1:
            bpy.ops.object.join()

    # We need to store our object in a variable to do actions on it.
    for object in MyScene.objects:
        if object.type == "MESH" and object.name != "Decor_Plane":
            bpy.data.objects[object.name].select_set(True)
            myobject=bpy.data.objects[object.name]


    #Check whether the object is correctly placed
    bpy.ops.object.transform_apply(location= False, rotation= True, scale=True)
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME')
    height = myobject.dimensions.z
    bottom = myobject.bound_box[0][2]

    if bottom < 0:

        bpy.ops.transform.translate(value=(0.0,0.0,(bottom*-1)))
        bottom = myobject.bound_box[0][2]



    myobject.location.x=0
    myobject.location.y=0
    myobject.location.z=bottom * -1

    #PLACE CAMERA CORRECTLY ON THE OBJECT
    bpy.ops.view3d.camera_to_view_selected()
    bpy.data.cameras.values()[0].lens = 25

#Use this function if you want to check that you have already rendered your object.
def Check(output_path, obj_name):
    Check.can_render = True
    Check.renderpath = output_path

    if not os.path.exists(Check.renderpath):
        os.makedirs(Check.renderpath)

    existing_renders = []
    existing_renders.extend(glob.glob(os.path.join(Check.renderpath, "**", "*.png"), recursive=True))
    Check.base_existing_rendername_list = []

    if len(existing_renders) == 0:
        Check.can_render=True

    else:
        for render in range (0, len(existing_renders)):
            existing_rendername = existing_renders[render]
            base_existing_rendername = os.path.join(obj_name, "_", "thumbnail")
            Check.base_existing_rendername_list.append(base_existing_rendername)


        for i in Check.base_existing_rendername_list:
            if obj_name in Check.base_existing_rendername_list:
                Check.can_render = False
                break

    return Check.can_render

def Render(output_path, obj_name):
    bpy.context.scene.render.filepath = os.path.join(output_path, obj_name + "_" + "thumbnail" + ".png")
    bpy.ops.render.render(write_still=True)

def Clean():
    bpy.ops.object.delete()
    bpy.data.cameras.values()[0].lens = Setup.default_fov

def ArgTest():
    print("HEYYYYYYY")
    print("1 is" + sys.argv[1])
    print("2 is" + sys.argv[2])
    print("3 is" + sys.argv[3])
    print("4 is" + sys.argv[4])
    print("5 is" + sys.argv[5])
    print("6 is" + sys.argv[6])
    print("7 is" + sys.argv[7])
    print("8 is" + sys.argv[8])
    print("9 is" + sys.argv[9])

Run()