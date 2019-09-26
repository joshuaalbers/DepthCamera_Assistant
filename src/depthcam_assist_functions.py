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