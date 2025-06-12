class MapHandler:
  unwrella_map_name = "Unwrella-IO"

  def set_map_name(name):
    MapHandler.unwrella_map_name = name

  def get_map_name():
    return MapHandler.unwrella_map_name

  def add_map_to_objects(objects):
    for obj in objects:
      if obj.type != "MESH":
        continue
      found = False
      for uv_layer in obj.data.uv_layers:
        if uv_layer.name == MapHandler.get_map_name():
          found = True
          continue
      if found == False:
        obj.data.uv_layers.new(name=MapHandler.get_map_name())
      obj.data.uv_layers.active = obj.data.uv_layers[MapHandler.get_map_name()]
    return

  def remove_map_from_objects(objects, name):
    for obj in objects:
      if obj.type != "MESH":
        continue
      uvs = obj.data.uv_layers
      if name in uvs:
        uvs.remove(uvs[name])
    return