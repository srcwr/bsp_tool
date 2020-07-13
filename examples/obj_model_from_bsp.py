import time
import sys

from utils import vector
sys.path.insert(0, "../")
import bsp_tool


def source_bsp_to_obj(bsp): #TODO: write .mtl for each vmt
    """yields an .obj file, one line at a time"""
    start_time = time.time()
    yield f"# Generated by bsp_tool from {bsp.filename}\n"
    vs = []
    v_count = 1
    vts = []
    vt_count = 1
    vns = []
    vn_count = 1
    faces_by_material = {} # {material: [face, ...], ...}
    disps_by_material = {} # {material: [face, ...], ...}
    for face_index, face in enumerate(bsp.FACES):
        tex_info = bsp.TEXINFO[face.tex_info]
        tex_data = bsp.TEXDATA[tex_info.tex_data]
        material = bsp.TEXDATA_STRING_DATA[tex_data.tex_data_string_index]
        if face.disp_info == -1:
            if material not in faces_by_material:
                faces_by_material[material] = []
            faces_by_material[material].append(face_index)
        else:
            if material not in disps_by_material:
                disps_by_material[material] = []
            disps_by_material[material].append(face_index)
    # FACES 
    face_number = 0
    current_progress = 0.1
    print("0...", end="")
    for material in faces_by_material:
        yield f"usemtl {material}\n"
        for face_index in faces_by_material[material]:
            face_vs = bsp.vertices_of_face(face_index)
            vn = face_vs[0][1]
            if vn not in vns:
                vns.append(vn)
                yield f"vn {vector.vec3(*vn):}\n"
                vn = vn_count
                vn_count += 1
            else:
                vn = vns.index(vn) + 1
            f = []
            for vertex in face_vs:
                v = vertex[0]
                if v not in vs:
                    vs.append(v)
                    yield f"v {vector.vec3(*v):}\n"
                    v = v_count
                    v_count += 1
                else:
                    v = vs.index(v) + 1
                vt = vertex[2]
                if vt not in vts:
                    vts.append(vt)
                    yield f"vt {vector.vec2(*vt):}\n"
                    vt = vt_count
                    vt_count += 1
                else:
                    vt = vts.index(vt) + 1
                f.append((v, vt, vn))
            yield "f " + ' '.join([f"{v}/{vt}/{vn}" for v, vt, vn in reversed(f)]) + "\n"
            face_number += 1
            if face_number >= len(bsp.FACES) * current_progress:
                print(f"{current_progress * 10:.0f}...", end="")
                current_progress += 0.1
    # DISPLACEMENTS
    disp_no = 0
    yield "g displacements\n"
    for material in disps_by_material:
        yield "usemtl {material}\n"
        for face_index in disps_by_material[material]:
            yield f"o displacement_{disp_no}\n"
            disp_no += 1
            disp_vs = bsp.vertices_of_displacement(face_index)
            normal = disp_vs[0][1]
            if normal not in vns:
                vns.append(normal)
                yield f"vn {vector.vec3(*normal):}\n"
                normal = vn_count
                vn_count += 1
            else:
                normal = vns.index(normal) + 1
            f = []
            for v, vn, vt, vt2, colour in disp_vs:
                yield f"v {vector.vec3(*v):}\nvt {vector.vec2(*vt):}\n"
            power = bsp.DISP_INFO[bsp.FACES[face_index].disp_info].power
            tris = bsp.mod.displacement_indices(power)
            for A, B, C in zip(tris[::3], tris[1::3], tris[2::3]):
                A = (A + v_count, A + vt_count, normal)
                B = (B + v_count, B + vt_count, normal)
                C = (C + v_count, C + vt_count, normal)
                A, B, C = [map(str, i) for i in (C, B, A)] # CCW FLIP
                yield f"f {'/'.join(A)} {'/'.join(B)} {'/'.join(C)}\n"
            disp_size = (2 ** power + 1) ** 2
            v_count += disp_size
            vt_count += disp_size
            face_count += 1
            if face_count >= total_faces * current_progress:
                print(f'{current_progress * 10:.0f}...', end='')
                current_progress += 0.1
    total_time = time.time() - start_time
    minutes = total_time // 60
    seconds = total_time - minutes * 60
    yield f"# file generated in {minutes:.0f} minutes {seconds:2.3f} seconds"
    print("Done!")
    print(f"Generated in {minutes:.0f} minutes {seconds:2.3f} seconds")


def respawn_bsp_to_obj(bsp): #TODO: write .mtl for each vmt
    """yields an .obj file, one line at a time"""
    start_time = time.time()
    yield f"# Generated by bsp_tool from {bsp.filename}\n"
    vts = []
    current_progress = 0.1
    print("0...", end="")
    for vertex in bsp.VERTICES:
        yield f"v {vertex.x} {vertex.y} {vertex.z}\n"
    for normal in bsp.VERTEX_NORMALS:
        yield f"vn {normal.x} {normal.y} {normal.z}\n"
    for mesh_index, mesh in enumerate(bsp.MESHES):
        yield f"o MESH_{mesh_index}\n"
        triangles = [] # [(v, vt, vn)]
        for vertex in bsp.vertices_of_mesh(mesh_index):
            if vertex.uv not in vts:
                yield f"vt {vertex.uv.u} {vertex.uv.v}\n"
                vt = len(vts)
            else:
                vt = vts.index(vertex.uv) + 1
            triangles.append((vertex.position_index + 1, vt, vertex.normal_index + 1))
        for A, B, C in zip(triangles[::3], triangles[1::3], triangles[2::3]):
            A, B, C = [map(str, i) for i in (C, B, A)] # CCW FLIP
            yield f"f {'/'.join(A)} {'/'.join(B)} {'/'.join(C)}\n"
        if mesh_index >= len(bsp.MESHES) * current_progress:
            print(f'{current_progress * 10:.0f}...', end='')
            current_progress += 0.1
    total_time = time.time() - start_time
    minutes = total_time // 60
    seconds = total_time - minutes * 60
    yield f"# file generated in {minutes:.0f} minutes {seconds:2.3f} seconds"
    print("Done!")
    print(f"Generated in {minutes:.0f} minutes {seconds:2.3f} seconds")


if __name__ == "__main__":
    import argparse
    ### THE FOLLOWING COMMAND LINE ARGS ARE PLANNED BUT UNIMPLEMETED ###
    # -g --game [apex_legends/team_fortess2/titanfall2/vindictus]
    # -o --outfile
    sys.argv.append("../maps/pl_upward.bsp")
    if len(sys.argv) > 1: # drag & drop obj converter
        write_obj = source_bsp_to_obj
        # ^ selected with --game
        for map_path in sys.argv[1:]:
            bsp = bsp_tool.bsp(map_path)
            obj_file = open(map_path + ".obj", "w")
            buffer = ""
            for line in write_obj(bsp):
                buffer += line
                if len(buffer) > 2048:
                    obj_file.write(buffer)
                    buffer = ""
            obj_file.write(buffer)
            obj_file.close()
    else:
        ... # do nothing (tests can go here)