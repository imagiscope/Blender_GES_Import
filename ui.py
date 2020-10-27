import bpy


class GESIO_OT_Paths(bpy.types.PropertyGroup):
    footage_path: bpy.props.StringProperty(name="footage_000",
                                           subtype='FILE_PATH',
                                           default=r"‪")

    json_path: bpy.props.StringProperty(name="JSON",
                                        subtype='FILE_PATH',
                                        default=r"‪")

    scale: bpy.props.FloatProperty(name="Scale", default=10)


class GESIO_PT_Panel(bpy.types.Panel):
    bl_idname = "gesio_PT_panel"
    bl_label = "Google Earth Studio"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "GES"

    def draw(self, context):
        layout = self.layout
        # layout.prop(gesio.scene_select, "filepath", text="")
        # layout.operator("gesio.scene_select")

        col = layout.column()
        row = col.row()
        row.label(text="First Image (*_000):")
        row = col.row()
        row.prop(bpy.context.scene.GESIO_OT_Paths, "footage_path", text="")

        col = layout.column()
        row = col.row()
        row.label(text="3D Tracking Data (.json):")
        row = col.row()
        row.prop(bpy.context.scene.GESIO_OT_Paths, "json_path", text="")

        row = col.row()
        row = col.row()
        row.prop(bpy.context.scene.GESIO_OT_Paths,
                 "scale",
                 text="Shrink Factor")

        row = col.row()
        row = col.row()
        row.operator("gesio.importscene", text="Import Scene", icon="IMPORT")


def register():
    bpy.types.Scene.GESIO_OT_Paths = bpy.props.PointerProperty(
        type=GESIO_OT_Paths)
