import enum

from .. import base
from .. import shared


BSP_VERSION = 29


class LUMP(enum.Enum):
    ENTITIES = 0
    PLANES = 1  # version 1
    TEXDATA = 2  # version 1
    VERTICES = 3
    UNUSED_4 = 4
    UNUSED_5 = 5
    UNUSED_6 = 6
    UNUSED_7 = 7
    UNUSED_8 = 8
    UNUSED_9 = 9
    UNUSED_10 = 10
    UNUSED_11 = 11
    UNUSED_12 = 12
    UNUSED_13 = 13
    MODELS = 14
    UNUSED_15 = 15
    UNUSED_16 = 16
    UNUSED_17 = 17
    UNUSED_18 = 18
    UNUSED_19 = 19
    UNUSED_20 = 20
    UNUSED_21 = 21
    UNUSED_22 = 22
    UNUSED_23 = 23
    ENTITY_PARTITIONS = 24
    UNUSED_25 = 25
    UNUSED_26 = 26
    UNUSED_27 = 27
    UNUSED_28 = 28
    PHYS_COLLIDE = 29
    VERTEX_NORMALS = 30
    UNUSED_31 = 31
    UNUSED_32 = 32
    UNUSED_33 = 33
    UNUSED_34 = 34
    GAME_LUMP = 35
    LEAF_WATERDATA = 36
    UNUSED_37 = 37
    UNUSED_38 = 38
    UNUSED_39 = 39
    PAKFILE = 40  # zip file, contains cubemaps
    UNKNOWN_41 = 41
    CUBEMAPS = 42
    TEXDATA_STRING_DATA = 43
    TEXDATA_STRING_TABLE = 44
    UNUSED_45 = 45
    UNUSED_46 = 46
    UNUSED_47 = 47
    UNUSED_48 = 48
    UNUSED_49 = 49
    UNUSED_50 = 50
    UNUSED_51 = 51
    UNUSED_52 = 52
    UNUSED_53 = 53
    WORLDLIGHTS_HDR = 54
    UNUSED_55 = 55
    UNUSED_56 = 56
    UNUSED_57 = 57
    UNUSED_58 = 58
    UNUSED_59 = 59
    UNUSED_60 = 60
    UNUSED_61 = 61
    PHYS_LEVEL = 62  # length 0, version 6?
    UNUSED_63 = 63
    UNUSED_64 = 64
    UNUSED_65 = 65
    TRICOLL_TRIS = 66
    UNUSED_67 = 67
    TRICOLL_NODES = 68
    TRICOLL_HEADERS = 69
    PHYSTRIS = 70
    VERTS_UNLIT = 71  # VERTS_RESERVED_0 - 7
    VERTS_LIT_FLAT = 72
    VERTS_LIT_BUMP = 73  # version 2
    VERTS_UNLIT_TS = 74
    VERTS_BLINN_PHONG = 75  # version 1
    VERTS_RESERVED_5 = 76  # version 1
    VERTS_RESERVED_6 = 77
    VERTS_RESERVED_7 = 78
    MESH_INDICES = 79  # version 1
    MESHES = 80  # version 1
    MESH_BOUNDS = 81
    MATERIAL_SORT = 82
    LIGHTMAP_HEADERS = 83
    LIGHTMAP_DATA_DXT5 = 84
    CM_GRID = 85
    CM_GRIDCELLS = 86
    CM_GEO_SETS = 87
    CM_GEO_SET_BOUNDS = 88
    CM_PRIMS = 89
    CM_PRIM_BOUNDS = 90  # version 1
    CM_UNIQUE_CONTENTS = 91
    CM_BRUSHES = 92
    CM_BRUSH_SIDE_PLANE_OFFSETS = 93
    CM_BRUSH_SIDE_PROPS = 94
    CM_BRUSH_TEX_VECS = 95
    TRICOLL_BEVEL_STARTS = 96
    TRICOLL_BEVEL_INDICES = 97
    LIGHTMAP_DATA_SKY = 98
    CSM_AABB_NODES = 99
    CSM_OBJ_REFS = 100
    LIGHTPROBES = 101
    STATIC_PROP_LIGHTPROBE_INDEX = 102
    LIGHTPROBE_TREE = 103
    LIGHTPROBE_REFS = 104
    LIGHTMAP_DATA_REAL_TIME_LIGHTS = 105
    CELL_BSP_NODES = 106
    CELLS = 107
    PORTALS = 108
    PORTAL_VERTS = 109
    PORTAL_EDGES = 110
    PORTAL_VERT_EDGES = 111
    PORTAL_VERT_REFS = 112
    PORTAL_EDGE_REFS = 113
    PORTAL_EDGE_ISECT_EDGE = 114
    PORTAL_EDGE_ISECT_AT_VERT = 115
    PORTAL_EDGE_ISECT_HEADER = 116
    OCCLUSION_MESH_VERTS = 117
    OCCLUSION_MESH_INDICES = 118
    CELL_AABB_NODES = 119
    OBJ_REFS = 120
    OBJ_REF_BOUNDS = 121
    UNKNOWN_122 = 122
    LEVEL_INFO = 123
    SHADOW_MESH_OPAQUE_VERTS = 124
    SHADOW_MESH_ALPHA_VERTS = 125
    SHADOW_MESH_INDICES = 126
    SHADOW_MESH_MESHES = 127


lump_header_address = {LUMP_ID: (16 + i * 16) for i, LUMP_ID in enumerate(LUMP)}


# classes for lumps (alphabetical order) [12 / 128] + 2 special lumps
class Brush(base.Struct):  # LUMP 92 (005C)
    __slots__ = ["normal", "unknown"]  # origin, id?
    _format = "3fI"  # not index & length into some list of planes?
    _arrays = {"normal": [*"xyz"]}


class MaterialSort(base.Struct):  # LUMP 82 (0052)
    __slots__ = ["texdata", "unknown", "vertex_offset"]
    _format = "2h2I"  # 12 bytes
    _arrays = {"unknown": [*"ab"]}


class Mesh(base.Struct):  # LUMP 80 (0050)
    __slots__ = ["start_index", "num_triangles", "unknown",
                 "material_sort", "flags"]
    # vertex type stored in flags
    _format = "IH3I2HI"  # 28 Bytes
    _arrays = {"unknown": [*"abcd"]}


class MeshIndices(int):  # LUMP 79 (004F)
    _format = "H"


class Model(base.Struct):  # LUMP 14 (000E)
    __slots__ = ["mins", "maxs", "first_mesh", "num_meshes"]
    _format = "6f2I"
    _arrays = {"mins": [*"xyz"], "maxs": [*"xyz"]}


class Plane(base.Struct):  # LUMP 1 (0001)
    __slots__ = ["normal", "distance"]
    _format = "4f"
    _arrays = {"normal": [*"xyz"]}


class ShadowMesh(base.Struct):  # LUMP 7F (0127)
    __slots__ = ["start_index", "num_triangles", "unknown"]
    _format = "2I2h"  # assuming 12 bytes
    _arrays = {"unknown": ["one", "negative_one"]}


class TextureData(base.Struct):  # LUMP 2 (0002)
    __slots__ = ["unknown", "string_table_index", "unknown2"]
    _format = "9i"
    _arrays = {"unknown": [*"abc"], "unknown2": [*"abcde"]}


class Vertex(base.MappedArray):  # LUMP 3 (0003)
    _mapping = [*"xyz"]
    _format = "3f"

    def flat(self):
        return [self.x, self.y, self.z]


class VertexBlinnPhong(base.Struct):  # LUMP 75 (004B)
    __slots__ = ["position_index", "normal_index", "unknown"]
    _format = "4I"  # 16 bytes
    _arrays = {"unknown": [*"ab"]}


class VertexLitBump(base.Struct):  # LUMP 71 (0047)
    __slots__ = ["position_index", "normal_index", "uv", "uv2", "uv3", "unknown"]
    # byte 8  - 12 = uv coords for albedo, normal, gloss & specular maps
    # byte 20 - 28 = uv coords for lightmap
    _format = "2I6f3I"  # 44 bytes
    _arrays = {"uv": [*"uv"], "uv2": [*"uv"], "uv3": [*"uv"],
               "unknown": [*"abc"]}


class VertexReserved5(base.Struct):  # LUMP 76 (004C)
    __slots__ = ["position_index", "normal_index", "unknown", "uv", "uv2"]
    _format = "7I4f"  # 44 bytes
    _arrays = {"unknown": [*"abcd"], "uv": [*"uv"], "uv2": [*"uv"]}


class VertexReserved7(base.Struct):  # LUMP 78 (004E)
    __slots__ = ["position_index", "normal_index", "uv", "negative_one"]
    _format = "2I2fi"  # 20 bytes
    _arrays = {"uv": [*"uv"]}


class VertexUnlit(base.Struct):  # LUMP 71 (0047)
    __slots__ = ["position_index", "normal_index", "uv", "unknown"]
    _format = "2I2fi"  # 20 bytes
    _arrays = {"uv": [*"uv"]}


class VertexUnlitTS(base.Struct):  # LUMP 74 (004A)
    __slots__ = ["position_index", "normal_index", "uv", "unknown"]
    _format = "2I2f3i"  # 28 bytes
    _arrays = {"uv": [*"uv"], "unknown": [*"abc"]}


LUMP_CLASSES = {"CM_BRUSHES": Brush,
                "MATERIAL_SORT": MaterialSort,
                "MODELS": Model,
                "PLANES": Plane,
                "TEXDATA": TextureData,
                "VERTEX_NORMALS": Vertex,
                "VERTICES": Vertex,
                "VERTS_LIT_BUMP": VertexLitBump,
                "VERTS_RESERVED_7": VertexReserved7,
                "VERTS_UNLIT": VertexUnlit,
                "VERTS_UNLIT_TS": VertexUnlitTS,
                "MESHES": Mesh,
                "MESH_INDICES": MeshIndices}

SPECIAL_LUMP_CLASSES = {"ENTITIES": shared.Entities,  # RespawnBsp uses shared.Entites to unpack the .ent files
                        "PAKFILE": shared.PakFile,
                        "TEXDATA_STRING_DATA": shared.TexDataStringData}


# branch exclusive methods, in alphabetical order:
mesh_types = {0x600: "VERTS_UNLIT_TS",
              0x400: "VERTS_UNLIT",
              0x200: "VERTS_LIT_BUMP"}
# ^ a proper mapping of the flags would be nice


# https://raw.githubusercontent.com/Wanty5883/Titanfall2/master/tools/TitanfallMapExporter.py
def vertices_of_mesh(bsp, mesh_index):  # simplified from McSimp's exporter ^
    """Vertex Format: (position.xyz, normal.xyz, uv.xy)"""
    mesh = bsp.MESHES[mesh_index]
    material_sort = bsp.MATERIAL_SORT[mesh.material_sort]
    start = mesh.start_index
    finish = start + mesh.num_triangles * 3
    indices = [material_sort.vertex_offset + i for i in bsp.MESH_INDICES[start:finish]]
    # TODO: cleaup these last 3 lines, the mesh_types dict is a wierd approach
    mesh_type = list(filter(lambda k: mesh.flags & k == k, mesh_types))[0]
    # ^ use mesh_types & mesh.flags with a bitmask to select the vertex lump
    verts = getattr(bsp, mesh_types[mesh_type])
    return [verts[i] for i in indices]


def vertices_of_model(bsp, model_index):
    # NOTE: model 0 is worldspawn, other models are referenced by entities
    out = ()
    model = bsp.MODELS[model_index]
    for i in range(model.first_mesh, model.num_meshes):
        out.extend(bsp.vertices_of_mesh(i))
    return out


methods = [vertices_of_mesh, vertices_of_model]
