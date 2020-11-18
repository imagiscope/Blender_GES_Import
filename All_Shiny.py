import bpy

sel = bpy.context.selected_objects
for i in sel:
    for mat in i.data.materials:
        mat.node_tree.nodes["Principled BSDF"].inputs["Specular"].default_value = 1.0
        mat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value0