# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "depthcamera_assistant",
    "author" : "Joshua Albers",
    "description" : "A plugin for converting depth camera images and sequences into geometry",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Mesh"
}

import bpy
import math

from bpy.props import (
	StringProperty,
	BoolProperty,
    FloatProperty,
	EnumProperty,
	PointerProperty,
	)

from bpy.types import (
	AddonPreferences,
	PropertyGroup,
	)

class DCA_Properties(PropertyGroup):
    distance_min: FloatProperty(
        name="Minimum distance", 
        description="Minimum distance to be included in processing",
        subtype='DISTANCE',
        default=0.0,
        min=0.0, # meters
        max=15.0,
        precision=5
    )

    distance_max: FloatProperty(
        name="Maximum distance", 
        description="Maximum distance to be included in processing",
        subtype='DISTANCE',
        default=15.0,
        min=0.0, # meters
        max=15.0,
        precision=5
    )

    distance_threshold: FloatProperty(
        name="Distance threshold",
        description="Maximum distance between points for mesh construction",
        subtype='DISTANCE',
        default=0.030, # meters
        min=0.0,
        max=1.0,
        precision=5,
    )

    object_name: StringProperty(
        name="Object name",
        description="Name of object to be created",
        default="DepthCam",
    )

from . depthcam_assist_operator import DCA_OT_Operator
from . depthcam_assist_panel import DCA_PT_Panel

classes = (
    DCA_OT_Operator,
    DCA_PT_Panel,
    DCA_Properties,
    )

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.dca = PointerProperty(type=DCA_Properties)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)