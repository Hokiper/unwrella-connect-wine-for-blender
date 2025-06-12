from bpy.types import PropertyGroup
from bpy.props import (BoolProperty, FloatProperty, EnumProperty)
from .app_params import (AppAccess, unwrellaParams)

class UnwrellaObjectProperties(PropertyGroup):

  def update_unwrap_mode(self, context):
    for obj in context.selected_objects:
      if obj.UnwrellaObjProps.uio_unwrap_mode != self.uio_unwrap_mode:
        obj.UnwrellaObjProps.uio_unwrap_mode = self.uio_unwrap_mode

  def update_pack_mode(self, context):
    for obj in context.selected_objects:
      if obj.UnwrellaObjProps.uio_pack_mode != self.uio_pack_mode:
        obj.UnwrellaObjProps.uio_pack_mode = self.uio_pack_mode

  def update_stretch(self, context):
    for obj in context.selected_objects:
      if obj.UnwrellaObjProps.uio_stretch != self.uio_stretch:
        obj.UnwrellaObjProps.uio_stretch = self.uio_stretch

  def update_hard_angle(self, context):
    for obj in context.selected_objects:
      if obj.UnwrellaObjProps.uio_hard_angle != self.uio_hard_angle:
        obj.UnwrellaObjProps.uio_hard_angle = self.uio_hard_angle

  def update_keep_seams(self, context):
    for obj in context.selected_objects:
      if obj.UnwrellaObjProps.uio_keep_seams != self.uio_keep_seams:
        obj.UnwrellaObjProps.uio_keep_seams = self.uio_keep_seams

  def update_use_marks(self, context):
    for obj in context.selected_objects:
      if obj.UnwrellaObjProps.uio_use_marks != self.uio_use_marks:
        obj.UnwrellaObjProps.uio_use_marks = self.uio_use_marks

  def update_cut_concave(self, context):
    for obj in context.selected_objects:
      if obj.UnwrellaObjProps.uio_cut_concave != self.uio_cut_concave:
        obj.UnwrellaObjProps.uio_cut_concave = self.uio_cut_concave

  def update_angle_concave(self, context):
    for obj in context.selected_objects:
      if obj.UnwrellaObjProps.uio_angle_concave != self.uio_angle_concave:
        obj.UnwrellaObjProps.uio_angle_concave = self.uio_angle_concave

  def update_cut_convex(self, context):
    for obj in context.selected_objects:
      if obj.UnwrellaObjProps.uio_cut_convex != self.uio_cut_convex:
        obj.UnwrellaObjProps.uio_cut_convex = self.uio_cut_convex

  def update_angle_convex(self, context):
    for obj in context.selected_objects:
      if obj.UnwrellaObjProps.uio_angle_convex != self.uio_angle_convex:
        obj.UnwrellaObjProps.uio_angle_convex = self.uio_angle_convex

  def update_cut_holes(self, context):
    for obj in context.selected_objects:
      if obj.UnwrellaObjProps.uio_cut_holes != self.uio_cut_holes:
        obj.UnwrellaObjProps.uio_cut_holes = self.uio_cut_holes

  def unwrapModesCallback(self, context):
    items=[
      ("0", "Organic", "Ideal for organic shapes with clean topology. Places UV seams along natural curves and relaxes UVs for minimal distortion and efficient texture usage.", unwrellaParams["icons"]["unwrap_organic"].icon_id, 0),
      ("1", "Hard Surface", "Optimized for sharp, angular geometry like mechanical forms and architecture. Offers fast unwrapping with minimal UV stretching.", unwrellaParams["icons"]["unwrap_hard"].icon_id, 1),
      ("2", "Mosaic", "Designed for complex, uneven geometry. Minimizes UV stretching and fragmentation, ideal for scans, triangulated, or rough models.", unwrellaParams["icons"]["unwrap_mosaic"].icon_id, 2),
      ("3", "Pack", "Packs and organizes all active UV data from selected objects or sub-objects to ensure a comprehensive and tidy UV arrangement.", unwrellaParams["icons"]["unwrap_pack"].icon_id, 3),
      ("4", "Keep Existing", "Keeps existing UV layouts intact, merging charts without modifying them. Best for finalized UVs; overlaps are not corrected automatically.", unwrellaParams["icons"]["unwrap_keep"].icon_id, 4),
    ]
    return items

  def packModesCallback(self, context):
    items=[
      ("0", "Pack", "Packs and organizes all active UV data from selected objects or sub-objects to ensure a comprehensive and tidy UV arrangement.", unwrellaParams["icons"]["unwrap_pack"].icon_id, 0),
      ("1", "Keep Existing", "Keeps existing UV layouts intact, merging charts without modifying them. Best for finalized UVs; overlaps are not corrected automatically.", unwrellaParams["icons"]["unwrap_keep"].icon_id, 1),
    ]
    return items

  uio_unwrap_mode: EnumProperty(
    name="Unwrap Mode:",
    description="Choose Unwrap Mode",
    items=unwrapModesCallback,
    default=1,
    update=update_unwrap_mode
  )
  uio_pack_mode: EnumProperty(
    name="Pack Mode:",
    description="Choose Pack Mode",
    items=packModesCallback,
    default=0,
    update=update_pack_mode
  )
  uio_stretch: FloatProperty(name="Stretch", description="Controls how much UV stretching is allowed to optimize texture distribution. 0 = no stretch, 1 = full stretch. (Only applicable when using the Organic or Mosaic unwrapping modes)", default = 0.15, min = 0.0, max = 1.0,
    update=update_stretch)
  uio_hard_angle: FloatProperty(name="Hard Angle", description="Maximum total angle a chart can bend.", default = 90.0, min = 0.0, max = 180.0,
    update=update_hard_angle)
  uio_keep_seams: BoolProperty(name="Keep Borders", description="If enabled, UV Borders will be considered during unwrapping to define island separation.", default = False, update=update_keep_seams)
  uio_use_marks: BoolProperty(name="Use Marks", description="If enabled, UV Marks will be considered during unwrapping to define the UV island borders.", default=True, update=update_use_marks)
  uio_cut_concave: BoolProperty(name="Cut Grooves", description="Use concave angles to automatically define where UV seams will be placed during unwrapping.", default = False, update=update_cut_concave)
  uio_angle_concave: FloatProperty(name="Groove Angle", description="Set the angle threshold; edges sharper than this value will be used to create UV cuts.", default = 45.0, min = 0.0, max = 180.0,
    update=update_angle_concave)
  uio_cut_convex: BoolProperty(name="Cut Ridges", description="Use convex angles to automatically define where UV seams will be placed during unwrapping.", default = False, update=update_cut_convex)
  uio_angle_convex: FloatProperty(name="Ridge Angle", description="Set the angle threshold; edges smoother than this value will be used to create UV cuts.", default = 45.0, min = 0.0, max = 180.0,
    update=update_angle_convex)
  uio_cut_holes: BoolProperty(name="Cut Holes", description="Automatically adds UV cuts around open holes to improve UV relaxation and distribution. Disable if unwanted seams appear.", default = True, update=update_cut_holes)