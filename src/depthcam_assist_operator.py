import bpy

class DEPTHCAMASSIST_OT_Operator(bpy.types.Operator):
    bl_idname = "view3d.depthcamera_assistant"
    bl_label = "simple operator"
    bl_description = "Do a depth camera assistant"

    def execute(self, context):
        print("Depth Camera Assistant EXECUTE")
        return {'FINISHED'}