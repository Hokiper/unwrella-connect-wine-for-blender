import bpy
import os
import platform
if (platform.system() == 'Windows'):
  import winreg
from .app_params import AppAccess

class Util:

  def get_meshes(objects):
    return [obj for obj in objects if obj.type=="MESH"]

  def get_unique_objects(objects):
    unique_meshes = []
    unique_objects = []
    for obj in objects:
      if obj.data in unique_meshes:
        continue
      unique_meshes.append(obj.data)
      unique_objects.append(obj)
    return unique_objects

  def show_message_box(message = "", title = "Message Box", icon = "INFO"):
    def draw(self, context):
      self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)
    return

  def get_app_path():
    if (platform.system() == 'Windows'):
      return Util.get_app_path_win()
    if (platform.system() == 'Darwin'):
      return Util.get_app_path_mac()
    return "", AppAccess.NONE

  def get_app_path_win():
    path = ""
    prefs = bpy.context.preferences.addons[__package__].preferences
    if (prefs):
      path = prefs.dirpath
    if (os.path.isfile(path + "/Unwrella-IO.exe")):
      return path + "/Unwrella-IO.exe", AppAccess.UNWRELLA_IO
    if (os.path.isfile(path + "/Packer-IO.exe")):
      return path + "/Packer-IO.exe", AppAccess.PACKER_IO
    path = Util.get_path_from_registry("Unwrella-IO")
    if (path):
      return path, AppAccess.UNWRELLA_IO
    path = Util.get_path_from_registry("Packer-IO")
    if (path):
      return path, AppAccess.PACKER_IO
    return "", AppAccess.NONE

  def get_app_path_mac():
    path = ""
    prefs = bpy.context.preferences.addons[__package__].preferences
    if (prefs):
      path = prefs.dirpath
    if (os.path.isfile(path + "Packer-IO.app/Contents/MacOS/Packer-IO")):
      return path + "Packer-IO.app/Contents/MacOS/Packer-IO", AppAccess.PACKER_IO
    path = "/Applications/Packer-IO.app/Contents/MacOS/Packer-IO"
    if (os.path.isfile(path)):
      return path, AppAccess.PACKER_IO
    path = os.getenv("HOME") + "/Applications/Packer-IO.app/Contents/MacOS/Packer-IO"
    if (os.path.isfile(path)):
      return path, AppAccess.PACKER_IO
    return path, AppAccess.NONE

  def get_path_from_registry(appName):
    try:
      key = winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE, fr"SOFTWARE\\3d-io\\{appName}\\")
      if key:
        path = winreg.QueryValueEx(key, "Executable")[0]
        winreg.CloseKey(key)
        return path
    except:
      return ""

  def get_scale_display_unit():
    unit = bpy.context.scene.unit_settings.length_unit
    if unit == "KILOMETERS":
      return "km"
    elif unit == "METERS":
      return "m"
    elif unit == "CENTIMETERS":
      return "cm"
    elif unit == "MILLIMETERS":
      return "mm"
    elif unit == "MICROMETERS":
      return "µm"
    elif unit == "MILES":
      return "mi"
    elif unit == "FEET":
      return "ft"
    elif unit == "INCHES":
      return "in"
    elif unit == "THOU":
      return "th"
    return "unit"