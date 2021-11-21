import sys
import bpy

path = sys.argv[-1]

bpy.ops.export_scene.obj(filepath=path,
                         check_existing=False,
                         # use_mesh_modifiers  = False,
                         # use_selection=False,
                         # axis_forward = '-Z',
                         # axis_up = 'Y',
                         )
