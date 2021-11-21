import sys
import bpy

legacy_mode = bpy.app.version < (2, 80, 0)

ignorable_object_types = ("EMPTY", "LAMP", "CAMERA")

stl_path = sys.argv[-1]


def deselect_all():
    # Deselect everything
    for ob in bpy.context.selected_objects:
        if legacy_mode:
            ob.select = False
        else:
            ob.select_set(False)


if legacy_mode:
    scene = bpy.context.scene
else:
    scene = bpy.context.view_layer

# Getting all children of all objects
children = []
for obj in scene.objects:
    for child in obj.children:
        children.append(child)

# Correcting normals of all objects
for obj in scene.objects:
    if obj.type in ignorable_object_types and obj not in children:
        continue

    print("Processing object {} of type: {}".format(repr(obj.name), obj.type))
    scene.objects.active = obj

    if legacy_mode:
        obj.select = True
    else:
        obj.select_set(True)

    mode_changed = False
    try:
        bpy.ops.object.mode_set(mode='EDIT')
        mode_changed = True
        # recalculate outside normals
        bpy.ops.mesh.normals_make_consistent(inside=False)
    except Exception:
        pass
    if mode_changed:
        # go object mode again
        bpy.ops.object.mode_set(mode='OBJECT')

    scene.update()

    deselect_all()

# Processing all objects
for obj in scene.objects:
    if obj.type in ignorable_object_types and obj not in children:
        continue

    print("Processing object {} of type: {}".format(repr(obj.name), obj.type))
    scene.objects.active = obj

    if legacy_mode:
        if not obj.hide:
            obj.select = True
    else:
        if not obj.hide_viewport:
            obj.select_set(True)

# Export everything at once
bpy.ops.export_mesh.stl(filepath=stl_path,
                        check_existing=False,
                        # use_mesh_modifiers  = True,
                        use_selection=True,
                        axis_forward='Y',
                        axis_up='Z',
                        # filter_glob="*.stl",
                        global_scale=1.0,
                        use_scene_unit=True,
                        # ascii=False,
                        # use_mesh_modifiers=True,
                        # batch_mode='OFF'
                        )
