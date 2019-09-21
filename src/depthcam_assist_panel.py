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

        row = layout.row()
        
        #row.prop(dca, "file_path", text="")
        layout.template_ID(sima, "image", open="image.open")
        #layout.operator("image.open", text="Open...", icon='FILE_FOLDER')

        row = layout.row()
        row.prop(dca, "reduce_factor", text="")

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