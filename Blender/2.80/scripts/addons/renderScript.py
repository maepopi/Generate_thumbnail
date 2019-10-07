import bpy
import os
import sys


#Cycles

bpy.context.scene.render.engine = 'CYCLES'


def run():
    rootfolder = os.path.join(sys.argv[4])
    obj_extension = os.path.join(sys.argv[5])
    obj_name = os.path.join(sys.argv[6])
    output_path = os.path.join(sys.argv[7])
    cyclo_path = os.path.join(sys.argv[8])
    hdri_path = os.path.join(sys.argv[9])



run()