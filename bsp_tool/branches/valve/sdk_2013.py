# https://github.com/ValveSoftware/source-sdk-2013/
import enum
from typing import List

from .. import base
# from . import alien_swarm
from . import left4dead2
from . import orange_box
from . import source


FILE_MAGIC = b"VBSP"

BSP_VERSION = 21

GAME_PATHS = {"Blade Symphony": "Blade Symphony/berimbau",
              "Counter-Strike: Global Offensive": "Counter-Strike Global Offensive/csgo",
              "Portal 2": "Portal 2/portal2",
              "Source Filmmaker": "Source Filmmaker/game/tf"}
# NOTE: also most sourcemods & mapbase

GAME_VERSIONS = {GAME_NAME: BSP_VERSION for GAME_NAME in GAME_PATHS}


# Counter-Strike Global Offensive/bin/bsppack.dll
class LUMP(enum.Enum):
    ENTITIES = 0
    PLANES = 1
    TEXTURE_DATA = 2
    VERTICES = 3
    VISIBILITY = 4
    NODES = 5
    TEXTURE_INFO = 6
    FACES = 7
    LIGHTING = 8
    OCCLUSION = 9
    LEAVES = 10
    FACE_IDS = 11
    EDGES = 12
    SURFEDGES = 13
    MODELS = 14
    WORLD_LIGHTS = 15
    LEAF_FACES = 16
    LEAF_BRUSHES = 17
    BRUSHES = 18
    BRUSH_SIDES = 19
    AREAS = 20
    AREA_PORTALS = 21
    FACE_BRUSHES = 22  # infra
    FACE_BRUSH_LIST = 23  # infra
    UNUSED_24 = 24
    UNUSED_25 = 25
    DISPLACEMENT_INFO = 26
    ORIGINAL_FACES = 27
    PHYSICS_DISPLACEMENT = 28
    PHYSICS_COLLIDE = 29
    VERTEX_NORMALS = 30
    VERTEX_NORMAL_INDICES = 31
    DISPLACEMENT_LIGHTMAP_ALPHAS = 32  # deprecated / X360 ?
    DISPLACEMENT_VERTICES = 33
    DISPLACEMENT_LIGHTMAP_SAMPLE_POSITIONS = 34
    GAME_LUMP = 35
    LEAF_WATER_DATA = 36
    PRIMITIVES = 37
    PRIMITIVE_VERTICES = 38  # deprecated / X360 ?
    PRIMITIVE_INDICES = 39
    PAKFILE = 40
    CLIP_PORTAL_VERTICES = 41
    CUBEMAPS = 42
    TEXTURE_DATA_STRING_DATA = 43
    TEXTURE_DATA_STRING_TABLE = 44
    OVERLAYS = 45
    LEAF_MIN_DIST_TO_WATER = 46
    FACE_MACRO_TEXTURE_INFO = 47
    DISPLACEMENT_TRIS = 48
    PROP_BLOB = 49  # left4dead
    WATER_OVERLAYS = 50  # deprecated / X360 ?
    LEAF_AMBIENT_INDEX_HDR = 51
    LEAF_AMBIENT_INDEX = 52
    LIGHTING_HDR = 53
    WORLD_LIGHTS_HDR = 54
    LEAF_AMBIENT_LIGHTING_HDR = 55
    LEAF_AMBIENT_LIGHTING = 56
    XZIP_PAKFILE = 57  # deprecated / X360 ?
    FACES_HDR = 58
    MAP_FLAGS = 59
    OVERLAY_FADES = 60
    OVERLAY_SYSTEM_LEVELS = 61  # left4dead
    PHYSICS_LEVEL = 62  # left4dead2
    DISPLACEMENT_MULTIBLEND = 63  # alienswarm


LumpHeader = source.LumpHeader

# TODO: Known lump changes from Orange Box -> Source SDK 2013:


# classes for special lumps, in alphabetical order:
class StaticPropv10(base.Struct):  # sprp GAME LUMP (LUMP 35) [version 10]
    """https://github.com/ValveSoftware/source-sdk-2013/blob/master/sp/src/public/gamebspfile.h#L186"""
    origin: List[float]  # origin.xyz
    angles: List[float]  # origin.yzx  QAngle; Z0 = East
    model_name: int  # index into GAME_LUMP.sprp.model_names
    first_leaf: int  # index into Leaf lump
    num_leafs: int  # number of Leafs after first_leaf this StaticProp is in
    solid_mode: int  # collision flags enum
    flags: int  # other flags
    skin: int  # index of this StaticProp's skin in the .mdl
    fade_distance: List[float]  # min & max distances to fade out
    lighting_origin: List[float]  # xyz position to sample lighting from
    forced_fade_scale: float  # relative to pixels used to render on-screen?
    cpu_level: List[int]  # min, max (-1 = any)
    gpu_level: List[int]  # min, max (-1 = any)
    diffuse_modulation: List[int]  # RGBA 32-bit colour
    disable_x360: bool
    flags_2: int  # values unknown
    __slots__ = ["origin", "angles", "name_index", "first_leaf", "num_leafs",
                 "solid_mode", "flags", "skin", "fade_distance", "lighting_origin",
                 "forced_fade_scale", "cpu_level", "gpu_level", "diffuse_modulation",
                 "disable_x360", "flags_2"]
    _format = "6f3H2Bi6f8B?I"
    _arrays = {"origin": [*"xyz"], "angles": [*"yzx"], "fade_distance": ["min", "max"],
               "lighting_origin": [*"xyz"], "cpu_level": ["min", "max"],
               "gpu_level": ["min", "max"], "diffuse_modulation": [*"rgba"]}


class StaticPropv11(base.Struct):  # sprp GAME LUMP (LUMP 35) [version 11]
    """https://github.com/ValveSoftware/source-sdk-2013/blob/master/sp/src/public/gamebspfile.h#L186"""
    origin: List[float]  # origin.xyz
    angles: List[float]  # origin.yzx  QAngle; Z0 = East
    model_name: int  # index into GAME_LUMP.sprp.model_names
    first_leaf: int  # index into Leaf lump
    num_leafs: int  # number of Leafs after first_leaf this StaticProp is in
    solid_mode: int  # collision flags enum
    flags: int  # other flags
    skin: int  # index of this StaticProp's skin in the .mdl
    fade_distance: List[float]  # min & max distances to fade out
    lighting_origin: List[float]  # xyz position to sample lighting from
    forced_fade_scale: float  # relative to pixels used to render on-screen?
    cpu_level: List[int]  # min, max (-1 = any)
    gpu_level: List[int]  # min, max (-1 = any)
    diffuse_modulation: List[int]  # RGBA 32-bit colour
    flags_2: int  # values unknown
    scale: float
    __slots__ = ["origin", "angles", "name_index", "first_leaf", "num_leafs",
                 "solid_mode", "flags", "skin", "fade_distance", "lighting_origin",
                 "forced_fade_scale", "cpu_level", "gpu_level", "diffuse_modulation",
                 "flags_2", "scale"]
    _format = "6f3H2Bi6f8BIf"
    _arrays = {"origin": [*"xyz"], "angles": [*"yzx"], "fade_distance": ["min", "max"],
               "lighting_origin": [*"xyz"], "cpu_level": ["min", "max"],
               "gpu_level": ["min", "max"], "diffuse_modulation": [*"rgba"]}


# {"LUMP_NAME": {version: LumpClass}}
BASIC_LUMP_CLASSES = orange_box.BASIC_LUMP_CLASSES.copy()

LUMP_CLASSES = orange_box.LUMP_CLASSES.copy()
LUMP_CLASSES.pop("WORLD_LIGHTS")
LUMP_CLASSES.pop("WORLD_LIGHTS_HDR")

SPECIAL_LUMP_CLASSES = orange_box.SPECIAL_LUMP_CLASSES.copy()

GAME_LUMP_HEADER = orange_box.GAME_LUMP_HEADER

GAME_LUMP_CLASSES = left4dead2.GAME_LUMP_CLASSES.copy()
GAME_LUMP_CLASSES["sprp"].update({10: lambda raw_lump: source.GameLump_SPRP(raw_lump, StaticPropv10),
                                  11: lambda raw_lump: source.GameLump_SPRP(raw_lump, StaticPropv11)})

methods = [*orange_box.methods]
