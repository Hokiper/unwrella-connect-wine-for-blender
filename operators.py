import bpy
from bpy.types import Operator
from .map_handler import MapHandler
from .processing import Processing

class UnwrapOperator(Operator):
  bl_idname = "unwrellaoperator.unwrapbtn"
  bl_label = "Unwrap"
  bl_options = {"REGISTER", "UNDO"}
  bl_description = "Unwrap selected objects"

  def execute(self, context):
    self.processing = Processing()
    return self.processing.execute(self, context)

  def modal(self, context, event):
    return self.processing.modal(self, context, event)

class QuickPackOperator(Operator):
  bl_idname = "unwrellaoperator.quickpackbtn"
  bl_label = "Quick Pack"
  bl_options = {"REGISTER", "UNDO"}
  bl_description = "Quickly pack selected objects with default settings"

  def execute(self, context):
    self.processing = Processing(True)
    return self.processing.execute(self, context)

  def modal(self, context, event):
    return self.processing.modal(self, context, event)

class SizeOperator(Operator):
  bl_idname = "unwrellaoperator.sizebtn"
  bl_label = "Size"
  bl_description = "UV Sheet dimension"
  size: bpy.props.IntProperty()

  def execute(self, context):
    context.scene.UnwrellaProps.uio_width = self.size
    context.scene.UnwrellaProps.uio_height = self.size
    return {"FINISHED"}

class RotationOperator(Operator):
  bl_idname = "unwrellaoperator.rotbtn"
  bl_label = "Rotation"
  rotation: bpy.props.IntProperty()

  def execute(self, context):
    context.scene.UnwrellaProps.uio_rotate = self.rotation
    return {"FINISHED"}

class FullRotationOperator(Operator):
  bl_idname = "unwrellaoperator.fullrotbtn"
  bl_label = "Full Rotation"

  def execute(self, context):
    context.scene.UnwrellaProps.uio_fullRotate = not context.scene.UnwrellaProps.uio_fullRotate
    return {"FINISHED"}

class ClearMapOperator(Operator):
  bl_idname = "unwrellaoperator.clearmaptoolbtn"
  bl_label = "Deletes the UV map data from the currently selected objects."
  bl_description = "Delete this UV map from the selected object(s)."

  def execute(self, context):
    name = context.scene.UnwrellaProps.uio_channel_name
    MapHandler.remove_map_from_objects(bpy.context.selected_objects, name)
    return {"FINISHED"}