from bpy.types import AddonPreferences
from bpy.props import StringProperty
from .app_params import unwrellaParams
from .util import Util

class UnwrellaPreferences(AddonPreferences):
  bl_idname = __package__

  def update_app_dir(self, context):
    unwrellaParams["appPath"], unwrellaParams["AppAccess"] = Util.get_app_path()

  def draw(self, context):
    layout = self.layout
    layout.label(text="If UnwrellaConnect can't find Unwrella-IO or Packer-IO correctly")
    layout.label(text="you can use this option to provide the directory manually.")
    layout.prop(self, "dirpath")

  dirpath: StringProperty(
    name = "Custom App Path",
    subtype = 'DIR_PATH',
    default = "",
    update = update_app_dir
  )