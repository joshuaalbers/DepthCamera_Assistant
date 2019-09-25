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
    "location" : "UV Editing",
    "warning" : "",
    "category" : "UV"
}

import bpy
import math

from bpy.props import (
	StringProperty,
	BoolProperty,
    IntProperty,
    FloatProperty,
	EnumProperty,
	PointerProperty,
	)

from bpy.types import (
	AddonPreferences,
	PropertyGroup,
	)

class DCA_Properties(PropertyGroup):
    reduce_factor: IntProperty(
        name="Reduce factor",
        description="Fraction by which to reduce resolution of calculated mesh",
        subtype="FACTOR",
        default=2, # 1 = 1/1, 2 = 1/2, 3 = 1/3, et cetera
        min=1,
        max=16
    )

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

    file_path: StringProperty(
        name="File path",
        description="Path to depth camera file(s)",
        subtype='FILE_PATH',
        default="",
    )

#from . depthcam_assist_functions import DCA_OT_Base
from . depthcam_assist_preview import DCA_OT_Preview
from . depthcam_assist_export import DCA_OT_Export
from . depthcam_assist_panel import DCA_PT_Panel

classes = (
    DCA_OT_Preview,
    DCA_OT_Export,
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