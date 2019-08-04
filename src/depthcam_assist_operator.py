import bpy
import math
import os
from itertools import zip_longest
from pathlib import Path

class DCA_OT_Preview(bpy.types.Operator):
    bl_idname = "view3d.dca_preview"
    bl_label = "preview operator"
    bl_description = "Preview the mesh of the current frame"

    def convertDistanceToXYZ(self, col, row, distance, w, h, unit_scale):
        # fov numbers from http://stackoverflow.com/questions/17832238/kinect-intrinsic-parameters-from-field-of-view
        hFov = math.radians(58.5)
        vFov = math.radians(45.6)
        xzFactor = math.tan(hFov/2) * 2
        yzFactor = math.tan(vFov/2) * 2
        normalizedX = col / w -0.5
        normalizedY = 0.5 - row / h
        x = normalizedX * xzFactor * distance * unit_scale
        y = normalizedY * yzFactor * distance * unit_scale * -1 # gotta flip Y to appease the transform gods
        z = distance * unit_scale
        output = (x, z, y)
        return( output )

    def execute(self, context):
        scene = context.scene
        dca = scene.dca

        if dca.file_path == "":
            print("You have to select an image file first.")
            return {'FINISHED'}

        print("Depth Camera Assistant EXECUTE\tValues:", dca.distance_min, dca.distance_max, dca.distance_threshold, dca.object_name, sep=', ', end='\n')
        scaleFactor = 100 # kludge to make the kinect data manageable
        width = 640
        height = 480
        reduceFactor = 1 #1 = 1/1, 2 = 1/2, 3 = 1/3, et cetera

        limitedDissolve = False
        
        inputPath = dca.file_path #don't forget the trailing /
        outfileBase = dca.object_name
        maxDistance = dca.distance_threshold #any neighboring vertices farther than this will not be meshed
        nearDistanceClip = dca.distance_min #any pixel depth smaller than this will not be used
        farDistanceClip = dca.distance_max #any pixel depth larger than this will not be used
        
        # outpathRoot = str(Path(inputPath).parents[0])+'/meshCache'
        # if not os.path.exists(outpathRoot):
        #     print('Creating '+outpathRoot)
        #     os.makedirs(outpathRoot)

        #https://blender.stackexchange.com/questions/23433/how-to-assign-a-new-material-to-an-object-in-the-scene-from-python#23434
        mat = bpy.data.materials.get("KinectMaterial")
        if mat is None:
            # create material
            mat = bpy.data.materials.new(name="KinectMaterial")

        #set the cursor to the origin
        bpy.data.scenes['Scene'].cursor.location[0] = 0
        bpy.data.scenes['Scene'].cursor.location[1] = 0
        bpy.data.scenes['Scene'].cursor.location[2] = 0

        bpy.data.images.load(inputPath)
        img = bpy.data.images[bpy.path.basename(inputPath)]
        (width, height) = img.size
        img.colorspace_settings.name="Raw" #we don't want no colorspace conversion for our distance data
        pixels = zip_longest(*[iter(img.pixels)]*4)
        distances = []
        for (r, g, b, a) in pixels: #blender converts single channel grayscale png to RGBA because why *not* use 4x the memory
            distances.append( r )
        points = []
        for i in range(0, len(distances), 1):
            r=i%width
            c=i/width
            #print(r, c)
            points.append(self.convertDistanceToXYZ(i%width, i/width, distances[i], width, height, scaleFactor))
        faces = [ ]
        for row in range(0, height-reduceFactor, reduceFactor):
            for col in range(0, width-reduceFactor, reduceFactor):
                index0 = col + (row * width)
                index1 = col + reduceFactor + (row * width)
                index2 = col + ((row + reduceFactor) * width)
                index3 = col + reduceFactor + ((row + reduceFactor) * width)
                distance01 = ( (points[index0][0] - points[index1][0])**2 + (points[index0][1] - points[index1][1] )**2 + (points[index0][2] - points[index1][2])**2 )**0.5
                distance02 = ( (points[index0][0] - points[index2][0])**2 + (points[index0][1] - points[index2][1] )**2 + (points[index0][2] - points[index2][2])**2 )**0.5
                distance13 = ( (points[index1][0] - points[index3][0])**2 + (points[index1][1] - points[index3][1] )**2 + (points[index1][2] - points[index3][2])**2 )**0.5
                distance23 = ( (points[index2][0]- points[index3][0])**2 + (points[index2][1] - points[index3][1] )**2 + (points[index2][2] - points[index3][2])**2 )**0.5
                isNWDistanceGood = (distance01 < maxDistance and distance02 < maxDistance)
                isSEDistanceGood = (distance13 < maxDistance and distance23 < maxDistance)   
                isPoint0Good = not (points[index0][0] == 0.0 and points[index0][1] == 0.0 and points[index0][2] == 0.0)
                isPoint1Good = not (points[index1][0] == 0.0 and points[index1][1] == 0.0 and points[index1][2] == 0.0)
                isPoint2Good = not (points[index2][0] == 0.0 and points[index2][1] == 0.0 and points[index2][2] == 0.0)
                isPoint3Good = not (points[index3][0] == 0.0 and points[index3][1] == 0.0 and points[index3][2] == 0.0)        
                if isPoint0Good and isPoint1Good and isPoint2Good and isNWDistanceGood:
                    #add connects for the NW triangle
                    faces.append((index0, index1, index2))       
                if isPoint1Good and isPoint2Good and isPoint3Good and isSEDistanceGood:
                    #add connects for the SE triangle
                    faces.append((index1, index3, index2))

        mesh = bpy.data.meshes.new(outfileBase)
        
        object = bpy.data.objects.new(outfileBase, mesh)
        object.location = bpy.context.scene.cursor.location
        # Link active object to the new collection
        bpy.context.collection.objects.link(object)
        bpy.context.view_layer.objects.active = object
        mesh.from_pydata(points, [], faces)
        mesh.update(calc_edges=True)

        if (object.select_get() is False):
            object.select_set(True)
        print("active_object = ", bpy.context.active_object)    
        bpy.ops.object.mode_set(mode='EDIT')
        
        if bpy.ops.mesh.select_all.poll():
            bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.remove_doubles(threshold=0.0001, use_unselected=False)
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_loose()
        bpy.ops.mesh.delete(type='VERT')
        bpy.ops.mesh.select_all(action='SELECT')
        if limitedDissolve:
            bpy.ops.mesh.dissolve_limited() #to try and reduce the polycount and file size
            bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
        if bpy.ops.object.mode_set.poll():
            bpy.ops.object.mode_set(mode='OBJECT')
        #new_object = bpy.context.object
        bpy.ops.object.shade_smooth()

        bpy.data.images.remove(img) #unload that image to make life better for everyone

        return {'FINISHED'}