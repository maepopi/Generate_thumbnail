import bpy
import os
import sys
import math
import glob



def Run():
    rootfolder = os.path.join(sys.argv[4])
    obj_extension = os.path.join(sys.argv[5])
    obj_name = os.path.join(sys.argv[6])
    output_path = os.path.join(sys.argv[7])
    studio_path = os.path.join(sys.argv[8])
    hdri_path = os.path.join(sys.argv[9])

  
    Setup(studio_path, hdri_path)
    Import(rootfolder, obj_extension)
    Place()

    # ArgTest()


def Setup(studio_path, hdri_path):
    #Setup scene and render engine
    Setup.MyScene = bpy.context.scene
    Setup.MyScene.render.engine = 'CYCLES'

    #Clean scene before render
    if "Cube" in Setup.MyScene.objects:
        bpy.data.objects["Cube"].select_set(True)
        bpy.ops.object.delete()

    if "Light" in Setup.MyScene.objects:
        bpy.data.objects["Light"].select_set(True)
        bpy.ops.object.delete()

    #Import studio
    bpy.ops.import_scene.obj(filepath = studio_path)


    #Lighting Setup
    Setup.MyScene.world.use_nodes = True
    world = Setup.MyScene.world
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

    Setup.MyScene.camera = Camera
    SetCamera(scene=Setup.MyScene, c=config)

    bpy.data.scenes["Scene"].cycles.use_denoising = True
    Setup.MyScene.render.resolution_x = 480
    Setup.MyScene.render.resolution_y= 270
    bpy.context.scene.render.resolution_percentage = 100

    Setup.default_fov = 35

def Import(rootfolder, obj_extension):
    candidate_object=rootfolder
    bpy.ops.import_scene.gltf(filepath=candidate_object, filter_glob="*.glb;*.gltf", import_pack_images=True)
    Import.my_object=bpy.context.selected_objects[0]
    Import.my_object.select_set(state=True)
    bpy.context.view_layer.objects.active = Import.my_object

def Place():
    # Check whether there are one or several objects, and unite all
    Objects_in_scene = []
    for object in Setup.MyScene.objects:
        if object.type == "MESH":
            Objects_in_scene.append(object)
        if len(Objects_in_scene)>1:
            bpy.ops.object.join()
    #Currently I can't get to join two objects in the scene
    
    # #Check whether the object is correctly placed
    # bpy.ops.object.transform_apply(location= False, rotation= True, scale=True)
    # bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME')
    # height = Import.my_object.dimensions.z
    # bottom = Import.my_object.bound_box[0][2]

    # if bottom < 0:
    
    #     bpy.ops.transform.translate(value=(0.0,0.0,(bottom*-1)))
    #     bottom = Import.my_object.bound_box[0][2]


    
    # Import.my_object.location.x=0
    # Import.my_object.location.y=0
    # Import.my_object.location.z=bottom * -1

    # #PLACE CAMERA CORRECTLY ON THE OBJECT
    # bpy.ops.view3d.camera_to_view_selected()
    # bpy.data.cameras.values()[0].lens = 25



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