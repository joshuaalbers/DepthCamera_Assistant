def convertDistanceToXYZ(col, row, distance, w, h, unit_scale):
    from math import radians, tan
    # fov numbers from http://stackoverflow.com/questions/17832238/kinect-intrinsic-parameters-from-field-of-view
    hFov = radians(58.5)
    vFov = radians(45.6)
    xzFactor = tan(hFov/2) * 2
    yzFactor = tan(vFov/2) * 2
    normalizedX = col / w -0.5
    normalizedY = 0.5 - row / h
    x = normalizedX * xzFactor * distance * unit_scale
    y = normalizedY * yzFactor * distance * unit_scale * -1 # gotta flip Y to appease the transform gods
    z = distance * unit_scale
    output = (x, z, y)
    return( output )

def image_sequence_resolve_all(filepath): #hey maybe I can delete this
    from os import path, scandir
    from string import digits
    basedir, filename = path.split(filepath)
    filename_noext, ext = path.splitext(filename)

    if isinstance(filepath, bytes):
        digits = digits.encode()
    filename_nodigits = filename_noext.rstrip(digits)

    if len(filename_nodigits) == len(filename_noext):
        # input isn't from a sequence
        return []

    return [
        f.path
        for f in scandir(basedir)
        if f.is_file() and
        f.name.startswith(filename_nodigits) and
        f.name.endswith(ext) and
        f.name[len(filename_nodigits):-len(ext) if ext else -1].isdigit()
    ]

# def image_to_mesh(depthimg, distmin, distmax, thresh, reduce):
#     (width, height) = depthimg.size
#         depthimg.colorspace_settings.name="Non-Color" #we don't want no colorspace conversion for our distance data
#         pixels = zip_longest(*[iter(depthimg.pixels)]*4)
#         distances = []
#         for (r, g, b, a) in pixels: #blender converts single channel grayscale png to RGBA because why *not* use 4x the memory
#             distances.append( r )
#         bpy.data.images.remove(depthimg) #unload that image to make life better for everyone

#         points = []
#         for i in range(0, len(distances), 1):
#             r=i%width
#             c=i/width
#             #print(r, c)
#             points.append(convertDistanceToXYZ(i%width, i/width, distances[i], width, height, scaleFactor))
#         faces = [ ]
#         for row in range(0, height-reduceFactor, reduceFactor):
#             for col in range(0, width-reduceFactor, reduceFactor):
#                 index0 = col + (row * width)
#                 index1 = col + reduceFactor + (row * width)
#                 index2 = col + ((row + reduceFactor) * width)
#                 index3 = col + reduceFactor + ((row + reduceFactor) * width)
#                 distance01 = ( (points[index0][0] - points[index1][0])**2 + (points[index0][1] - points[index1][1] )**2 + (points[index0][2] - points[index1][2])**2 )**0.5
#                 distance02 = ( (points[index0][0] - points[index2][0])**2 + (points[index0][1] - points[index2][1] )**2 + (points[index0][2] - points[index2][2])**2 )**0.5
#                 distance13 = ( (points[index1][0] - points[index3][0])**2 + (points[index1][1] - points[index3][1] )**2 + (points[index1][2] - points[index3][2])**2 )**0.5
#                 distance23 = ( (points[index2][0]- points[index3][0])**2 + (points[index2][1] - points[index3][1] )**2 + (points[index2][2] - points[index3][2])**2 )**0.5
#                 isNWDistanceGood = (distance01 < maxDistance and distance02 < maxDistance)
#                 isSEDistanceGood = (distance13 < maxDistance and distance23 < maxDistance)   
#                 isPoint0Good = (points[index0]!=[0.0, 0.0, 0.0] and points[index0][1] > nearDistanceClip and points[index0][1] < farDistanceClip)
#                 isPoint1Good = (points[index1]!=[0.0, 0.0, 0.0] and points[index1][1] > nearDistanceClip and points[index1][1] < farDistanceClip)
#                 isPoint2Good = (points[index2]!=[0.0, 0.0, 0.0] and points[index2][1] > nearDistanceClip and points[index2][1] < farDistanceClip)
#                 isPoint3Good = (points[index3]!=[0.0, 0.0, 0.0] and points[index3][1] > nearDistanceClip and points[index3][1] < farDistanceClip)       
#                 if isPoint0Good and isPoint1Good and isPoint2Good and isNWDistanceGood:
#                     #add connects for the NW triangle
#                     faces.append((index0, index1, index2))       
#                 if isPoint1Good and isPoint2Good and isPoint3Good and isSEDistanceGood:
#                     #add connects for the SE triangle
#                     faces.append((index1, index3, index2))