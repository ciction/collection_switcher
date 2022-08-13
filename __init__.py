# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
import bpy
from bpy.types import (Panel, Operator)
from bpy.props import StringProperty


bl_info = {
    "name" : "Collection_switcher",
    "author" : "Christophe Swolfs",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

# main_collection = 'Opstellingen Living'


# class MyProperties(bpy.types.PropertyGroup):
#     my_float: bpy.props.FloatProperty(name = "Float", description = "Enter a float", soft_min = -100, soft_max = 100 )


# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------

class SimpleOperator(bpy.types.Operator):
    """Print object name in Console"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"
    
    text: bpy.props.StringProperty(
    name = 'calling Button',
    default = 'test'
    )


    def execute(self, context):
#       my parent colletion
        parentCollection = bpy.context.scene.my_collection_property  #bpy.data.collections[main_collection]
        childCollections = parentCollection.children_recursive
        for collection in childCollections:
            collection.hide_viewport = True
        bpy.data.collections[self.text].hide_viewport = False
            
        
        
        
        print(self.text)
        # print (context.object)
        return {'FINISHED'}

# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------

class OBJECT_PT_CustomPanel(Panel):
    bl_idname = "object.custom_panel"
    bl_label = "Isolate Collection"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Tools"
    bl_context = "objectmode"   

    # my_collection_property: bpy.props.StringProperty()    #second way of declaring property
    




    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        scene = context.scene
        # myProperties = scene.myProperties

        layout = self.layout
        obj = context.object

        layout.label(text="Select the parent collection:")

        # col = layout.column(align=True)
        # layout.row().prop(obj, "collection", text="Line Set Collection")
        col = layout.column(align=True)
        col.prop(context.scene, "my_collection_property", text="Parent Collection")

        # row = layout.row(align=True)
        # row.prop(obj, "show_name", toggle=True, icon="FILE_FONT")
        # row.prop(obj, "show_wire", toggle=True, text="Wireframe", icon="SHADING_WIRE")
        # row.prop(obj, "show_all_edges", toggle=True, text="Show all Edges", icon="MOD_EDGESPLIT")
        layout.separator()

        layout.label(text="Isolate child collection:")

        col = layout.column(align=True)
        parentCollection = scene.my_collection_property  #bpy.data.collections[main_collection]
        childCollections = parentCollection.children_recursive
        for collection in childCollections:
            op = col.operator(SimpleOperator.bl_idname, text=collection.name)
            op.text = collection.name
                        
        layout.separator()

# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

# classes = [OBJECT_PT_CustomPanel,SimpleOperator, MyProperties]
classes = [OBJECT_PT_CustomPanel,SimpleOperator]

def register():
    bpy.types.Scene.my_collection_property = bpy.props.PointerProperty(type=bpy.types.Collection) #third way with property pointer
    
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # bpy.types.Scene.my_collection_property = bpy.props.StringProperty()        #first way of declaring property

    #make property global?
    # bpy.types.Scene.myProperties = bpy.props.PointerProperty(type = MyProperties)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()