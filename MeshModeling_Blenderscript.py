import sys
if not dir in sys.path:
    sys.path.append(r"/path/to/your/directory/")
    sys.path.append(r"/path/to/your/directory/")
    print(sys.path)
import bpy
from utils.blender_tools import initialize, clearMesh
from utils.AnnotationImport import importPoints
from utils.MeshBuilding import getMeshSplines, bridgeLoopMeshes, reloc_entrypoint, smoothingLines, getnsaveMeshOpenSplines

def main():

    # blender initialization
    initialize()
    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 0.001

    # subject number
    sub_num = 'sub-num'

    # target nerveroots and their radius
    SEG = ["L1", "L2", "L3", "L4", "L5", "S1", "S2"]
    Rs = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

    # data import
    annotation_base_path = r'/path/to/your/directory/'
    dura, cord, lines = importPoints(annotation_base_path, SEG, sub_num)

    # dura mesh building 
    getMeshSplines(dura, "Dura")
    bridgeLoopMeshes("Dura", sub_num)
    clearMesh()

    # cord mesh building
    getMeshSplines(cord, "Cord")
    bridgeLoopMeshes("Cord", sub_num)
    clearMesh()

    # nerveroots mesh building
    cordstl_path = f"output\{sub_num}_Cord.stl"
    lines_relocated = reloc_entrypoint(cordstl_path, lines)
    lines_smoothed = smoothingLines(lines_relocated, n_interpolate = 100, s=10)
    getnsaveMeshOpenSplines(lines_smoothed, SEG, Rs, sub_num)

    # preparation for manual sculpting in blender
    bpy.ops.import_mesh.stl(filepath=f'output\{sub_num}_Dura.stl')
    bpy.ops.import_mesh.stl(filepath=f'output\{sub_num}_Cord.stl')


main()
