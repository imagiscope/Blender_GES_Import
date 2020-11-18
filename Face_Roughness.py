import bpy
import bmesh

obj = bpy.context.edit_object
me = obj.data
bm = bmesh.from_edit_mesh(me)
sel = bpy.context.active_object

for f in bm.faces:
    if f.select:
        mat = me.materials[f.material_index]
        # shiny = 0.0, not shiny = 1.0
        sel.data.materials[mat.name].node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 1.0

bmesh.update_edit_mesh(me, True)