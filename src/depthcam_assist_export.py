import bpy
import math
import os
from itertools import zip_longest
from pathlib import Path
from . depthcam_assist_functions import convertDistanceToXYZ, image_sequence_resolve_all

class DCA_OT_Export(bpy.types.Operator):
    bl_idname = "mesh.dca_export"
    bl_label = "export operator"
    bl_description = "Export the mesh sequence"

    def execute(self, context):
        scene = context.scene
        dca = scene.dca
        img=context.space_data.image
        imguser=context.space_data.image_user
        limitedDissolve = False

        originalname=img.name
        img.name='original'
       
        scaleFactor = 100 # kludge to make the kinect data look right
        reduceFactor = dca.reduce_factor #1 = 1/1, 2 = 1/2, 3 = 1/3, et cetera

        if bpy.ops.object.select_all.poll():
            bpy.ops.object.select_all(action='DESELECT')
        
        outfileBase = dca.object_name
        outpathRoot = str(Path(bpy.path.abspath(img.filepath)).parents[1])+'/meshCache'
        if not os.path.exists(outpathRoot):
            print('DEPTH CAM ASSIST: Creating '+outpathRoot)
            os.makedirs(outpathRoot)

        #https://blender.stackexchange.com/questions/23433/how-to-assign-a-new-material-to-an-object-in-the-scene-from-python#23434
        mat = bpy.data.materials.get("ScanMaterial")
        if mat is None:
            # create material
            mat = bpy.data.materials.new(name="ScanMaterial")
        
        for i in range(imguser.frame_start, imguser.frame_start + imguser.frame_duration):
            maxDistance = dca.distance_threshold #any neighboring vertices farther than this will not be meshed
            nearDistanceClip = dca.distance_min #any pixel distance smaller than this will not be used
            farDistanceClip = dca.distance_max #any pixel distance larger than this will not be used
            
            scene.frame_set(i)
            imguser.frame_current=i

            print("TESTING: ", scene.frame_current, imguser.frame_current, img.filepath_from_user(image_user=imguser))
            depthimg=bpy.data.images.load(img.filepath_from_user(image_user=imguser))

            (width, height) = depthimg.size
            depthimg.colorspace_settings.name="Non-Color" #we don't want no colorspace conversion for our distance data
            pixels = zip_longest(*[iter(depthimg.pixels)]*4)
            distances = []
            for (r, g, b, a) in pixels: #blender converts single channel grayscale png to RGBA because why *not* use 4x the memory
                distances.append( r )
            points = []
            for i in range(0, len(distances), 1):
                r=i%width
                c=i/width
                #print(r, c)
                points.append(convertDistanceToXYZ(i%width, i/width, distances[i], width, height, scaleFactor))
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
                    isPoint0Good = (points[index0]!=[0.0, 0.0, 0.0] and points[index0][1] > nearDistanceClip and points[index0][1] < farDistanceClip)
                    isPoint1Good = (points[index1]!=[0.0, 0.0, 0.0] and points[index1][1] > nearDistanceClip and points[index1][1] < farDistanceClip)
                    isPoint2Good = (points[index2]!=[0.0, 0.0, 0.0] and points[index2][1] > nearDistanceClip and points[index2][1] < farDistanceClip)
                    isPoint3Good = (points[index3]!=[0.0, 0.0, 0.0] and points[index3][1] > nearDistanceClip and points[index3][1] < farDistanceClip)       
                    if isPoint0Good and isPoint1Good and isPoint2Good and isNWDistanceGood:
                        #add connects for the NW triangle
                        faces.append((index0, index1, index2))       
                    if isPoint1Good and isPoint2Good and isPoint3Good and isSEDistanceGood:
                        #add connects for the SE triangle
                        faces.append((index1, index3, index2))

            mesh = bpy.data.meshes.new(outfileBase)
            
            object = bpy.data.objects.new(outfileBase, mesh)
            object.location = bpy.context.scene.cursor.location
            bpy.context.collection.objects.link(object) # Link active object to the new collection
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
            bpy.ops.object.shade_smooth()

            outfileName = outpathRoot+'/'+outfileBase+"_%05d.abc"%(imguser.frame_current)
            print("Saving " + outfileName)
            bpy.ops.wm.alembic_export(filepath=outfileName, start=imguser.frame_current, end=imguser.frame_current+1, selected=True, as_background_job=False)
            bpy.ops.object.delete() #delete the object so we don't cram our memory too much
            bpy.data.images.remove(depthimg) #unload that image to make life better for everyone
        
        img.name=originalname

        return {'FINISHED'}