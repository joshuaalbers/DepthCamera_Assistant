import bpy

class DCA_OT_Operator(bpy.types.Operator):
    bl_idname = "view3d.depthcamera_assistant"
    bl_label = "simple operator"
    bl_description = "Do a depth camera assistant"

    def execute(self, context):
        scene = context.scene
        dca = scene.dca
        print("Depth Camera Assistant EXECUTE\tValues:", dca.distance_min, dca.distance_max, dca.distance_threshold, dca.object_name, sep=', ', end='\n')
        return {'FINISHED'}