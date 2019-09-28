import bpy

class DCA_PT_Panel(bpy.types.Panel):
    bl_idname = "DCA_PT_Assistant_Panel"
    bl_label = "Depth Camera Assistant Panel"
    #bl_category = "Depth Camera Assistant"
    # bl_space_type = "VIEW_3D"
    # bl_region_type = "UI"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Depth Cam Assist"

    #bl_context ="imagepaint"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        dca = scene.dca
        sima = context.space_data
        ima = sima.image

        layout.template_ID(sima, "image", open="image.open")
        if ima:
            row = layout.row()
            row.prop(dca, "reduce_factor", text="Reduce Factor")

            row = layout.row()
            row.prop(dca, "distance_min", text="Min Distance")

            row = layout.row()
            row.prop(dca, "distance_max", text="Max Distance")

            row = layout.row()
            row.prop(dca, "distance_threshold", text="Point Threshold")

            row = layout.row()
            row.prop(scene, "frame_current", text="Current Scene Frame")

            row = layout.row()
            row.prop(dca, "object_name", text="Object Name")

            row = layout.row()
            row.prop(dca, "limited_dissolve", text="Limited Dissolve", toggle=True)

            row = layout.row()
            row.operator("mesh.dca_preview", text = "Preview Frame")

            row = layout.row()
            row.prop(dca, "export_start_frame", text="Export Start Frame")

            row = layout.row()
            row.prop(dca, "export_duration", text="Export Duration")

            row = layout.row()
            row.label(text="Export path:")
            row.prop(dca, "export_path", text="")

            row = layout.row()
            row.operator("mesh.dca_export", text = "Export Sequence")