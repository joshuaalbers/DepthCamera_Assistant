import bpy

class DEPTHCAMASSIST_PT_Panel(bpy.types.Panel):
    bl_idname = "DepthCamera_Assistant_Panel"
    bl_label = "Depth Camera Assistant Panel"
    bl_category = "Depth Camera Assistant"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator('view3d.depthcamera_assistant', text = "Depth Camera Assistant")