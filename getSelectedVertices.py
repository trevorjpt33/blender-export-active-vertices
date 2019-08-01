import bpy
from bpy.types import Menu, Operator
import bmesh
import sys
from pathlib import Path as plib

bl_info = {
    "name": "Vertex ID Storage Tool",
    "author": "Trevor Poirier",
    "description": "Copy vertex selection data to a new text file in your Documents folder",
    "location": "VIEW3D_MT_edit_mesh",
    "category": "Mesh"}

docs = str(plib.home().joinpath('Documents'))
destfile = str(docs) + '//blendSelection.txt'

def getBlendVerts(self, context):

    self.ob = bpy.context.active_object
    self.mymesh = self.ob.data
    bm = bmesh.from_edit_mesh(self.mymesh)

    allVerts = [i for i in bm.verts]
    selectedVerts = []

    for vert in allVerts:
        if vert.select == True:
            selectedVerts.append(vert.index)

    blend_vertSel = sorted(selectedVerts)

    blendIn = str(blend_vertSel)
    blendIn = blendIn.translate({ord(i): r',' for i in r']'})
    blendOut = blendIn.translate({ord(i): None for i in r' []'})

    print('The', len(blend_vertSel), 'vertex IDs in your Blender selection saved.')
    print('Check "boneAssign_tool" folder for a file named "blendSelection.txt".')

    return blendOut


def store_bvertsFile_w(self, context):
    with open(destfile, 'w') as f:

        bverts_data = getBlendVerts(self, context)
        stopsys = sys.stdout
        f.seek(0,0)
        sys.stdout = f
        print(bverts_data)

        sys.stdout = stopsys
        f.close()


def store_bvertsFile_a(self, context):
    with open(destfile, 'a') as f:

        bverts_data = getBlendVerts(self, context)
        stopsys = sys.stdout
        f.seek(0,0)
        sys.stdout = f
        print(bverts_data)

        sys.stdout = stopsys
        f.close()


class makeButton(Menu):
    bl_idname = "VIEW3D_MT_edit_mesh_vstore"
    bl_label = ("2K19 CF Convert Kit")
    def draw(self, context):
        self.layout.operator("mesh.vstore_write", text="Overwrite Vertex ID Data")
        self.layout.operator("mesh.vstore_append", text="Append Vertex ID Data")


class storeVertexID_write(Operator):
    bl_idname = "mesh.vstore_write"
    bl_label = ("Vertex IDs to File")
    bl_description = "Click to write a new text file with vertex ID data."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        store_bvertsFile_w(self, context)
        return {'FINISHED'}


class storeVertexID_append(Operator):
    bl_idname = "mesh.vstore_append"
    bl_label = ("Vertex IDs to File")
    bl_description = "Click to append vertex ID data to an existing text file."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        store_bvertsFile_a(self, context)
        return {'FINISHED'}


def createMenu(self, context):
    self.layout.menu("VIEW3D_MT_edit_mesh_vstore", icon="SCRIPTPLUGINS")


def register():
    bpy.utils.register_class(storeVertexID_write)
    bpy.utils.register_class(storeVertexID_append)
    bpy.utils.register_class(makeButton)
    bpy.types.VIEW3D_MT_edit_mesh.append(createMenu)


def unregister():
    bpy.utils.unregister_class(storeVertexID_write)
    bpy.utils.unregister_class(storeVertexID_append)
    bpy.utils.unregister_class(makeButton)
    bpy.types.VIEW3D_MT_edit_mesh.remove(createMenu)


if __name__ == "__main__":
    register()
