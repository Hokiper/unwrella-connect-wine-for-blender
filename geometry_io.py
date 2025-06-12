import bpy
import bmesh
import struct
from .app_params import (AppAccess, unwrellaParams)
from .face_data import FaceData

class GeometryIO:

  def gather_geometry_data(meshes, localOptions):
    allObjectData = bytearray()
    usedFaces = {}
    for object_idx, obj in enumerate(meshes):
      objectData, usedObjFaces = GeometryIO.gather_object_data(object_idx, obj, localOptions)
      if len(objectData) > 0:
        allObjectData += objectData
        usedFaces[object_idx] = usedObjFaces

    data = bytearray()
    data += (len(usedFaces)).to_bytes(4, byteorder="little")
    data += allObjectData
    return data, usedFaces

  def gather_object_data(object_idx, obj, localOptions):
    bm = bmesh.from_edit_mesh(obj.data)
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    keepSeams = obj.UnwrellaObjProps.uio_keep_seams
    if (obj.data.uv_layers.active == None):
      obj.data.uv_layers.new(name=bpy.context.scene.UnwrellaProps.uio_channel_name)
      keepSeams = False
    uvLayer = bm.loops.layers.uv.verify()

    syncmode = bpy.context.scene.tool_settings.use_uv_select_sync
    usedObjFaces = []
    indexCount = numUvVertices = numGeoIndices = numUvIndices = numPolygons = numPinned = numCustomSeams = 0
    uvVertexData, geoIndexData, uvIndexData = bytearray(), bytearray(), bytearray()
    polygonData, pinnedData, customSeamData = bytearray(), bytearray(), bytearray()
    for i, face in enumerate(bm.faces):
      data, indexCount = GeometryIO.gather_face_data(face, uvLayer, indexCount, localOptions["Selection"], syncmode)
      if (data):
        numUvVertices += len(data.uvVertices)
        for uvVertex in data.uvVertices:
          uvVertexData += bytearray(struct.pack("<dd", uvVertex[0], uvVertex[1]))
        numGeoIndices += len(data.geoIndices)
        for geoIndex in data.geoIndices:
          geoIndexData += geoIndex.to_bytes(4, byteorder="little")
        numUvIndices += len(data.uvIndices)
        for uvIndex in data.uvIndices:
          uvIndexData += uvIndex.to_bytes(4, byteorder="little")
        numPolygons += 1
        polygonData += (len(face.loops)).to_bytes(4, byteorder="little")
        if data.isPinned:
          numPinned += 1
          pinnedData += i.to_bytes(4, byteorder="little")
        usedObjFaces.append(i)

    if obj.UnwrellaObjProps.uio_use_marks:
      for edge in bm.edges:
        if edge.seam:
          numCustomSeams += 1
          customSeamData += (edge.verts[0].index).to_bytes(4, byteorder="little")
          customSeamData += (edge.verts[1].index).to_bytes(4, byteorder="little")

    objectData = bytearray()
    if numPolygons > 0:
      objectData += GeometryIO.encode_object_metadata(object_idx, obj, localOptions["QuickPack"], keepSeams)
      objectData += (len(bm.verts)).to_bytes(4, byteorder="little")
      for vert in bm.verts:
        objectData += bytearray(struct.pack("<ddd", vert.co.x, vert.co.y, vert.co.z))

      objectData += numUvVertices.to_bytes(4, byteorder="little")
      objectData += uvVertexData
      objectData += numGeoIndices.to_bytes(4, byteorder="little")
      objectData += geoIndexData
      objectData += numUvIndices.to_bytes(4, byteorder="little")
      objectData += uvIndexData
      objectData += numPolygons.to_bytes(4, byteorder="little")
      objectData += polygonData
      objectData += numPinned.to_bytes(4, byteorder="little")
      objectData += pinnedData
      objectData += numCustomSeams.to_bytes(4, byteorder="little")
      objectData += customSeamData

    return objectData, usedObjFaces

  def encode_object_metadata(object_idx, obj, quickPack, keepSeams):
    metadata = bytearray()
    metadata += (object_idx).to_bytes(4, byteorder="little")
    nameBytes = obj.name.encode()
    metadata += (len(nameBytes)).to_bytes(4, byteorder="little")
    metadata.extend(nameBytes)
    if (unwrellaParams["AppAccess"] == AppAccess.UNWRELLA_IO and quickPack):
      metadata += int(3).to_bytes(4, byteorder="little")
    elif (unwrellaParams["AppAccess"] == AppAccess.UNWRELLA_IO):
      metadata += int(obj.UnwrellaObjProps.uio_unwrap_mode).to_bytes(4, byteorder="little")
    elif (quickPack):
      metadata += int(0).to_bytes(4, byteorder="little")
    else:
      metadata += int(obj.UnwrellaObjProps.uio_pack_mode).to_bytes(4, byteorder="little")
    metadata += bytearray(struct.pack("<d", obj.UnwrellaObjProps.uio_stretch))
    metadata += bytearray(struct.pack("<d", obj.UnwrellaObjProps.uio_hard_angle))
    metadata += bytearray(struct.pack("<?", keepSeams))
    metadata += bytearray(struct.pack("<?", obj.UnwrellaObjProps.uio_cut_concave))
    metadata += bytearray(struct.pack("<d", obj.UnwrellaObjProps.uio_angle_concave))
    metadata += bytearray(struct.pack("<?", obj.UnwrellaObjProps.uio_cut_convex))
    metadata += bytearray(struct.pack("<d", obj.UnwrellaObjProps.uio_angle_convex))
    metadata += bytearray(struct.pack("<?", obj.UnwrellaObjProps.uio_cut_holes))
    return metadata

  def gather_face_data(face, uvLayer, indexCount, selectionOnly, syncmode):
    if selectionOnly and syncmode and not face.select:
        return None, indexCount

    adjustedindexCount = indexCount
    faceData = FaceData()
    faceData.deg = len(face.loops)
    for loop in face.loops:
      if selectionOnly and not syncmode and not loop[uvLayer].select:
        return None, indexCount

      uv_coord = loop[uvLayer].uv
      faceData.uvVertices.append([uv_coord.x, uv_coord.y])
      faceData.geoIndices.append(loop.vert.index)
      faceData.uvIndices.append(adjustedindexCount)
      adjustedindexCount += 1
      if loop[uvLayer].pin_uv:
        faceData.isPinned = True

    return faceData, adjustedindexCount

  def update_object_data(obj, message, readPtr, selectionOnly, usedObjFaces):
    bm = bmesh.from_edit_mesh(obj.data)
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    uvLayer = bm.loops.layers.uv.verify()

    resultVertices = []
    numResultVertices = struct.unpack_from("<I", message, readPtr)[0]
    readPtr += 4
    for v in range(0, numResultVertices):
      x = struct.unpack_from("<d", message, readPtr)[0]
      readPtr += 8
      y = struct.unpack_from("<d", message, readPtr)[0]
      readPtr += 8
      resultVertices.append([x, y])

    resultIndices = []
    numResultIndices = struct.unpack_from("<I", message, readPtr)[0]
    readPtr += 4
    for v in range(0, numResultIndices):
      resultIndices.append(struct.unpack_from("<I", message, readPtr)[0])
      readPtr += 4

    idx = 0
    currentUsedFaceIndex = 0
    finalUsedFace = len(usedObjFaces) - 1
    for i, face in enumerate(bm.faces):
      if not selectionOnly or i == usedObjFaces[currentUsedFaceIndex]:
        if currentUsedFaceIndex < finalUsedFace:
          currentUsedFaceIndex += 1
        for loop in face.loops:
          loop[uvLayer].uv = resultVertices[resultIndices[idx]]
          idx += 1

    bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)
    return readPtr