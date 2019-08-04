import bpy

class DCA_PT_Panel(bpy.types.Panel):
    bl_idname = "DCA_PT_Assistant_Panel"
    bl_label = "Depth Camera Assistant Panel"
    bl_category = "Depth Camera Assistant"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        dca = scene.dca

        row = layout.row()
        row.prop(dca, "file_path", text="")

        row = layout.row()
        row.prop(dca, "distance_min", text="")

        row = layout.row()
        row.prop(dca, "distance_max", text="")

        row = layout.row()
        row.prop(dca, "distance_threshold", text="")

        row = layout.row()
        row.prop(dca, "object_name", text="")

        row = layout.row()
        row.operator("view3d.dca_preview", text = "Preview")