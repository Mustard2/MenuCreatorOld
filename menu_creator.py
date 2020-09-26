bl_info = {
    "name": "Menu Creator",
    "description": "A tool to create custom UI from the list of properties of an object",
    "author": "Mustard",
    "version": (0, 0, 1),
    "blender": (2, 90, 1),
    "warning": "",
    "category": "3D View",
}

import bpy
from bpy.props import *

# ------------------------------------------------------------------------
#    Settings and functions classes
# ------------------------------------------------------------------------

# Global addon settings properties class
class ObjProp_AddonSettings(bpy.types.PropertyGroup):
    active : bpy.props.BoolProperty(default = True,
                                            name="Active Object",
                                            description="Show the menu only for the active object.\nIf disabled, some settings will appear in the Menu Settings to set up a multi-object UI")
    
    global_name: bpy.props.StringProperty(name="UI Name", default="UI")
    global_row_scale: bpy.props.FloatProperty(name="Row Scale", default=1.0)
    
    description : bpy.props.BoolProperty(default = False,
                                            name="Properties Description",
                                            description="Show properties description.\nAn information button will be added for each property, showing the description and additional informations")
    visibility_filter : bpy.props.BoolProperty(default = False,
                                            name="Properties Visibility Filter",
                                            description="Enable custom property visibility filters.\nNote that disabling this you will have access to more properties, but drastically increase the number of properties shown")
    
    debug : bpy.props.BoolProperty(default = False,
                                            name="Debug mode",
                                            description="Enable Debug mode.\nThis will write more messages in the console, to help debug errors.\nEnable it only if needed, because it can decrease the performance")
    debug_verbose : bpy.props.IntProperty(default = 1,
                                            min = 1,
                                            max = 3,
                                            name="Debug mode verbosity",
                                            description="Change Debug mode verbosity.\nBigger values will make the addon more talkative in the console")
bpy.utils.register_class(ObjProp_AddonSettings)

# Properties property (one for each property added)
class ObjProp_Property(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Property Name", default="")
    identifier : bpy.props.StringProperty(name="Identifier", default="")
    type : bpy.props.StringProperty(name="Property Type", default="")
    type_identifier : bpy.props.StringProperty(name="Type Identifier", default="")
bpy.utils.register_class(ObjProp_Property)

# Menu properties (one for each object selected)
class ObjProp_MenuSettings(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="UI Name", default="UI")
    show_no_active : bpy.props.BoolProperty(name="", default=False)
    show_obj_name: bpy.props.BoolProperty(name="Show Object Name", default=True)
    row_scale: bpy.props.FloatProperty(name="Row Scale", default=1.0)
bpy.utils.register_class(ObjProp_MenuSettings)
    
bpy.types.Scene.ObjProp_settings = PointerProperty(type=ObjProp_AddonSettings)
bpy.types.Object.ObjProp_menu = PointerProperty(type=ObjProp_MenuSettings)
bpy.types.Object.ObjProp_properties = CollectionProperty(type=ObjProp_Property)

# Class of functions for manipulation of collections
class ObjProp_CollectionPropFunctions():
    
    def add_prop(collection, item):
        
        i=True
        
        for el in collection:
            if el.identifier==item[0]:
                i=False
                break
        if i:
            add_item = collection.add()
            add_item.name = item[0]
            add_item.identifier = item[1]
            add_item.type = item[2]
            add_item.type_identifier = item[3]
    
    def remove_prop(collection, item):
        
        i=-1
        for el in collection:
            i=i+1
            if el.identifier==item[0] and el.type==item[1] and el.type_identifier==item[2]:
                break
        collection.remove(i)
    
    def index_prop(collection, item):
        
        i=-1
        for el in collection:
            i=i+1
            if el.identifier==item[0] and el.type==item[1] and el.type_identifier==item[2]:
                break
        return i
    
    def check_prop(collection, item):
        i=False
        for el in collection:
            if el.identifier==item[0] and el.type==item[1] and el.type_identifier==item[2]:
                i=True
                break
        return i
    
    def swap_prop(collection, pos1, pos2):
      
        collection.move(pos1,pos2)
        return list
    
    def len_collection(collection):
        i=0
        for el in collection:
            i=i+1
        return i
    
    def clean_prop(obj):
        obj.ObjProp_properties.clear()
    
    def clean_all_prop():
        for obj in bpy.data.objects:
            obj.ObjProp_properties.clear()
            
    def print_prop(obj):
        print("OBJPROP DEBUG: Properties found")
        for el in obj.ObjProp_properties:
            print("     " + "Name: " + el.name + ". Identifier: " + el.identifier + ". Type: " + el.type + ". Type id: " + el.type_identifier)
        print("\n")

# Class for storing filters
class ObjProp_PropertyFilters():
    object_visibility_filter = ["location",
                        "scale",
                        "display_type",
                        "show_wire",
                        "show_in_front"]
    material_visibility_filter = ["blend_method",
                        "use_screen_refraction",
                        "show_transparent_back",
                        "use_backface_culling",
                        "use_nodes",
                        "diffuse_color","specular_color",
                        "roughness","specular","metallic"]
    light_visibility_filter = ["type",
                        "color",
                        "distance",
                        "energy",
                        "shadow_soft_size",
                        "use_custom_distance",
                        "shadow_buffer_clip_start",
                        "shadow_buffer_bias",
                        "cutoff_distance",
                        "use_contact_shadow",
                        "contact_shadow_distance",
                        "contact_shadow_bias",
                        "contact_shadow_thickness"]

# ------------------------------------------------------------------------
#    Menu Operations
# ------------------------------------------------------------------------

class OBJPROP_OT_AddProperty(bpy.types.Operator):
    """Add the property to the menu"""
    bl_idname = "objprop.add_prop"
    bl_label = ""
    bl_options = {'REGISTER'}
    
    prop_name : bpy.props.StringProperty(default="")
    prop_id : bpy.props.StringProperty(default="")
    prop_type : bpy.props.StringProperty(default="")
    prop_type_id : bpy.props.StringProperty(default="")
    
    def execute(self, context):
        
        scene = context.scene
        settings = scene.ObjProp_settings
        
        obj = bpy.context.object
        
        ObjProp_CollectionPropFunctions.add_prop(obj.ObjProp_properties,[self.prop_name,self.prop_id,self.prop_type,self.prop_type_id])
        
        if settings.debug and settings.debug_verbose > 1:
            ObjProp_CollectionPropFunctions.print_prop(obj)
        
        return {'FINISHED'}

class OBJPROP_OT_RemoveProperty(bpy.types.Operator):
    """Remove the property from the menu"""
    bl_idname = "objprop.remove_prop"
    bl_label = ""
    bl_options = {'REGISTER'}
    
    prop_id : bpy.props.StringProperty(default="")
    prop_type : bpy.props.StringProperty(default="")
    prop_type_id : bpy.props.StringProperty(default="")
    
    def execute(self, context):
        
        scene = context.scene
        settings = scene.ObjProp_settings
        
        obj = bpy.context.object
        
        ObjProp_CollectionPropFunctions.remove_prop(obj.ObjProp_properties,[self.prop_id,self.prop_type,self.prop_type_id])
        
        if settings.debug and settings.debug_verbose > 1:
            ObjProp_CollectionPropFunctions.print_prop(obj)
        
        return {'FINISHED'}

class OBJPROP_OT_MoveProperty(bpy.types.Operator):
    """Move the property in the menu property list"""
    bl_idname = "objprop.move_prop"
    bl_label = ""
    bl_options = {'REGISTER'}
    
    prop_id1 : bpy.props.IntProperty()
    prop_id2 : bpy.props.IntProperty()
    
    def execute(self, context):
        
        scene = context.scene
        settings = scene.ObjProp_settings
        
        obj = bpy.context.object
        
        ObjProp_CollectionPropFunctions.swap_prop(obj.ObjProp_properties,self.prop_id1,self.prop_id2)
        
        if settings.debug and settings.debug_verbose > 1:
            ObjProp_CollectionPropFunctions.print_prop(obj)
        
        return {'FINISHED'}

class OBJPROP_OT_DescriptionProperty(bpy.types.Operator):
    """Description of the property"""
    bl_idname = "objprop.description_prop"
    bl_label = "Property Informations"
    bl_options = {'REGISTER'}
    
    description : bpy.props.StringProperty(default="")
    identifier : bpy.props.StringProperty(default="")
    type : bpy.props.StringProperty(default="")
    
    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width = 750)

    def draw(self, context):
        layout = self.layout
        
        layout.label(text="Description", icon="INFO")
        box = layout.box()
        if self.description!="":
            box.label(text=self.description+".")
        else:
            box.label(text="No description available.")
        
        layout.label(text="Identifier", icon="RNA")
        box = layout.box()
        box.label(text=self.identifier)
        
        layout.label(text="Type", icon="LINENUMBERS_ON")
        box = layout.box()
        box.label(text=self.type)
    

class OBJPROP_OT_CleanProperty(bpy.types.Operator):
    """Clean all the property from the menu"""
    bl_idname = "objprop.clean_prop"
    bl_label = "Clean properties"
    bl_options = {'REGISTER'}
    
    active: bpy.props.BoolProperty(default=True)
    
    def execute(self, context):
        
        if self.active:
            obj = bpy.context.object
        
            ObjProp_CollectionPropFunctions.clean_prop(obj)
        
        else:
            ObjProp_CollectionPropFunctions.clean_all_prop()
        
        return {'FINISHED'}

# ------------------------------------------------------------------------
#    Panel
# ------------------------------------------------------------------------

class MainPanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Menu Creator"
    #bl_options = {"DEFAULT_CLOSED"}


class OBJPROP_PT_List(MainPanel, bpy.types.Panel):
    bl_idname = "OBJPROP_PT_LIST"
    bl_label = "Properties Selection"
    
    @classmethod
    def poll(self,context):
        return context.object is not None
    
    def draw(self, context):
        
        layout = self.layout
        scene = context.scene
        settings = scene.ObjProp_settings
        
        obj = context.object
        
        selected_object = "Selected object: " + obj.name
        layout.label(text=selected_object, icon = obj.type+"_DATA")

class OBJPROP_PT_List_General(MainPanel, bpy.types.Panel):
    bl_parent_id = "OBJPROP_PT_LIST"
    bl_label = "General"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        
        layout = self.layout
        scene = context.scene
        settings = scene.ObjProp_settings
        
        obj = context.object
        
        box = layout.box()
        
        index=[]
        for prop in obj.ObjProp_properties:
            if ((settings.visibility_filter and prop.identifier in ObjProp_PropertyFilters.object_visibility_filter) or not settings.visibility_filter) and prop.type == "OBJECT":
                index.append( ObjProp_CollectionPropFunctions.index_prop(obj.ObjProp_properties,[prop.identifier,prop.type, prop.type_identifier]) )       
                
        for prop in obj.ObjProp_properties:
            if ((settings.visibility_filter and prop.identifier in ObjProp_PropertyFilters.object_visibility_filter) or not settings.visibility_filter) and prop.type == "OBJECT":
                row = box.row()
                row.label(text=prop.name)
                
                id1 = index.index( ObjProp_CollectionPropFunctions.index_prop(obj.ObjProp_properties,[prop.identifier,prop.type, prop.type_identifier]) )
                row2 = row.row(align=True)
                if id1>0:
                    op = row2.operator("objprop.move_prop",icon="TRIA_UP")
                    op.prop_id1=index[id1-1]
                    op.prop_id2=index[id1]
                else:
                    col = row2.column(align=True)
                    col.enabled=False
                    col.operator("objprop.move_prop",icon="TRIA_UP")
                if id1<len(index)-1:
                    op = row2.operator("objprop.move_prop",icon="TRIA_DOWN")
                    op.prop_id1=index[id1]
                    op.prop_id2=index[id1+1]
                else:
                    col = row2.column(align=True)
                    col.enabled=False
                    col.operator("objprop.move_prop",icon="TRIA_DOWN")
                
                op = row.operator("objprop.remove_prop",icon="REMOVE")
                op.prop_id = prop.identifier
                op.prop_type = "OBJECT"
                op.prop_type_id = ""
        
        if len(index) > 0:
            box.separator()
        
        for prop in obj.rna_type.properties:
            if (settings.visibility_filter and prop.identifier in ObjProp_PropertyFilters.object_visibility_filter) or not settings.visibility_filter:
                if settings.debug and settings.debug_verbose > 2:
                    print("Property name: {}".format(prop.name))
                    print("Property RNA name: {}".format(prop.identifier))
                    print("      Value: {} \n".format(eval("obj."+prop.identifier)))
                if not prop.is_readonly:
                        row = box.row()
                        row.label(text=prop.name)
                        if not ObjProp_CollectionPropFunctions.check_prop(obj.ObjProp_properties, [prop.identifier,"OBJECT",""]):
                            op = row.operator("objprop.add_prop",icon="ADD")
                            op.prop_name = prop.name
                            op.prop_id = prop.identifier
                            op.prop_type = "OBJECT"
                            op.prop_type_id = ""
                        else:
                            op = row.operator("objprop.remove_prop",icon="REMOVE")
                            op.prop_id = prop.identifier
                            op.prop_type = "OBJECT"
                            op.prop_type_id = ""
                        if settings.description:
                            op = row.operator("objprop.description_prop",icon="INFO",text="")
                            op.description = prop.description
                            op.identifier = prop.identifier
                            op.type = prop.type

class OBJPROP_PT_List_Materials(MainPanel, bpy.types.Panel):
    bl_parent_id = "OBJPROP_PT_LIST"
    bl_label = "Materials"
    bl_options = {"DEFAULT_CLOSED"}
    
    @classmethod
    def poll(self,context):
        obj = context.object
        if obj.type == "MESH":
            return True
        else:
            return False

    def draw(self, context):
        
        layout = self.layout
        scene = context.scene
        settings = scene.ObjProp_settings
        
        obj = context.object
                
        for mat in obj.data.materials:
            box = layout.box()
            box.label(text=mat.name,icon="MATERIAL")
            if settings.debug and settings.debug_verbose > 2:
                print("Material: {} \n".format(mat.name))
                
            index=[]
            for prop in obj.ObjProp_properties:
                if ((settings.visibility_filter and prop.identifier in ObjProp_PropertyFilters.material_visibility_filter) or not settings.visibility_filter) and prop.type == "MATERIAL" and prop.type_identifier == mat.name:
                    index.append( ObjProp_CollectionPropFunctions.index_prop(obj.ObjProp_properties,[prop.identifier,prop.type, prop.type_identifier]) )
            
            for prop in obj.ObjProp_properties:
                if ((settings.visibility_filter and prop.identifier in ObjProp_PropertyFilters.material_visibility_filter) or not settings.visibility_filter) and prop.type == "MATERIAL" and prop.type_identifier == mat.name:
                    row = box.row()
                    row.label(text=prop.name)
                    
                    id1 = index.index( ObjProp_CollectionPropFunctions.index_prop(obj.ObjProp_properties,[prop.identifier,prop.type, prop.type_identifier]) )
                    row2 = row.row(align=True)
                    if id1>0:
                        op = row2.operator("objprop.move_prop",icon="TRIA_UP")
                        op.prop_id1=index[id1-1]
                        op.prop_id2=index[id1]
                    else:
                        col = row2.column(align=True)
                        col.enabled=False
                        col.operator("objprop.move_prop",icon="TRIA_UP")
                    if id1<len(index)-1:
                        op = row2.operator("objprop.move_prop",icon="TRIA_DOWN")
                        op.prop_id1=index[id1]
                        op.prop_id2=index[id1+1]
                    else:
                        col = row2.column(align=True)
                        col.enabled=False
                        col.operator("objprop.move_prop",icon="TRIA_DOWN")
                    
                    op = row.operator("objprop.remove_prop",icon="REMOVE")
                    op.prop_id = prop.identifier
                    op.prop_type = "MATERIAL"
                    op.prop_type_id = mat.name
            
            if len(index) > 0:
                box.separator()
            
            for prop in bpy.data.materials[mat.name].rna_type.properties:
                if (settings.visibility_filter and prop.identifier in ObjProp_PropertyFilters.material_visibility_filter) or not settings.visibility_filter:
                    if settings.debug and settings.debug_verbose > 2:
                        print("Property name: {}".format(prop.name))
                        print("Property RNA name: {}".format(prop.identifier))
                        print("      Value: {} \n".format(eval("bpy.data.materials[mat.name]."+prop.identifier)))
                    if not prop.is_readonly:
                        if not ObjProp_CollectionPropFunctions.check_prop(obj.ObjProp_properties, [prop.identifier,"MATERIAL",mat.name]):
                            row = box.row()
                            row.label(text=prop.name)
                            op = row.operator("objprop.add_prop",icon="ADD")
                            op.prop_name = prop.name
                            op.prop_id = prop.identifier
                            op.prop_type = "MATERIAL"
                            op.prop_type_id = mat.name
                            if settings.description:
                                op = row.operator("objprop.description_prop",icon="INFO",text="")
                                op.description = prop.description
                                op.identifier = prop.identifier
                                op.type = prop.type
                

class OBJPROP_PT_List_Lights(MainPanel, bpy.types.Panel):
    bl_parent_id = "OBJPROP_PT_LIST"
    bl_label = "Light"
    bl_options = {"DEFAULT_CLOSED"}
    
    @classmethod
    def poll(self,context):
        obj = context.object
        if obj.type == "LIGHT":
            return True
        else:
            return False

    def draw(self, context):
        
        layout = self.layout
        scene = context.scene
        settings = scene.ObjProp_settings
        
        obj = context.object
        lig = obj
                
        box = layout.box()
        
        index=[]
        for prop in obj.ObjProp_properties:
            if ((settings.visibility_filter and prop.identifier in ObjProp_PropertyFilters.light_visibility_filter) or not settings.visibility_filter) and prop.type == "LIGHT" and prop.type_identifier == lig.name:
                index.append( ObjProp_CollectionPropFunctions.index_prop(obj.ObjProp_properties,[prop.identifier,prop.type, prop.type_identifier]) )
        
        for prop in obj.ObjProp_properties:
            if ((settings.visibility_filter and prop.identifier in ObjProp_PropertyFilters.material_visibility_filter) or not settings.visibility_filter) and prop.type == "LIGHT" and prop.type_identifier == lig.name:
                row = box.row()
                row.label(text=prop.name)
                
                id1 = index.index( ObjProp_CollectionPropFunctions.index_prop(obj.ObjProp_properties,[prop.identifier,prop.type, prop.type_identifier]) )
                row2 = row.row(align=True)
                if id1>0:
                    op = row2.operator("objprop.move_prop",icon="TRIA_UP")
                    op.prop_id1=index[id1-1]
                    op.prop_id2=index[id1]
                else:
                    col = row2.column(align=True)
                    col.enabled=False
                    col.operator("objprop.move_prop",icon="TRIA_UP")
                if id1<len(index)-1:
                    op = row2.operator("objprop.move_prop",icon="TRIA_DOWN")
                    op.prop_id1=index[id1]
                    op.prop_id2=index[id1+1]
                else:
                    col = row2.column(align=True)
                    col.enabled=False
                    col.operator("objprop.move_prop",icon="TRIA_DOWN")
                
                op = row.operator("objprop.remove_prop",icon="REMOVE")
                op.prop_id = prop.identifier
                op.prop_type = "MATERIAL"
                op.prop_type_id = mat.name
        
        if len(index) > 0:
            box.separator()
        
        for prop in bpy.data.lights[lig.name].rna_type.properties:
            if (settings.visibility_filter and prop.identifier in ObjProp_PropertyFilters.light_visibility_filter) or not settings.visibility_filter:
                if settings.debug and settings.debug_verbose > 2:
                    print("Property name: {}".format(prop.name))
                    print("Property RNA name: {}".format(prop.identifier))
                    print("      Value: {} \n".format(eval("bpy.data.lights[lig.name]."+prop.identifier)))
                if not prop.is_readonly:
                    row = box.row()
                    row.label(text=prop.name)
                    if not ObjProp_CollectionPropFunctions.check_prop(obj.ObjProp_properties, [prop.identifier,"LIGHT",lig.name]):
                        op = row.operator("objprop.add_prop",icon="ADD")
                        op.prop_name = prop.name
                        op.prop_id = prop.identifier
                        op.prop_type = "LIGHT"
                        op.prop_type_id = lig.name
                    else:
                        op = row.operator("objprop.remove_prop",icon="REMOVE")
                        op.prop_id = prop.identifier
                        op.prop_type = "LIGHT"
                        op.prop_type_id = lig.name
                    if settings.description:
                        op = row.operator("objprop.description_prop",icon="INFO",text="")
                        op.description = prop.description
                        op.identifier = prop.identifier
                        op.type = prop.type

class OBJPROP_PT_MenuSettings(MainPanel, bpy.types.Panel):
    bl_idname = "OBJPROP_PT_MENUSETTINGS"
    bl_label = "Menu Settings"
    
    @classmethod
    def poll(self,context):
        return context.object is not None
    
    def draw(self, context):
        
        obj = context.object
        
        layout = self.layout
        scene = context.scene
        settings = obj.ObjProp_menu
        addon_settings = scene.ObjProp_settings
        
        layout.label(text="Graphics", icon="TOPBAR")
        box=layout.box()
        if addon_settings.active:
            box.prop(settings,"show_obj_name")
        if addon_settings.active:
            box.prop(settings,"row_scale")
        else:
            box.prop(addon_settings,"global_row_scale")
        
        layout.label(text="Name", icon="OUTLINER_DATA_FONT")
        box=layout.box()
        if addon_settings.active:
            box.prop(settings,"name")
        else:
            box.prop(addon_settings,"global_name")
        box.label(text="Applied after restart", icon="INFO")
        
        if not addon_settings.active:
            for objs in bpy.data.objects:
                if ObjProp_CollectionPropFunctions.len_collection(objs.ObjProp_properties)>0:
                    layout.label(text="Objects with properties found",icon="OBJECT_DATA")
                    box=layout.box()
                    break
                
            for objs in bpy.data.objects:
                if ObjProp_CollectionPropFunctions.len_collection(objs.ObjProp_properties)>0:
                    row=box.row()
                    row.label(text=objs.name)
                    if objs.ObjProp_menu.show_no_active:
                        row.prop(objs.ObjProp_menu, "show_no_active", icon="REMOVE")
                    else:
                        row.prop(objs.ObjProp_menu, "show_no_active", icon="ADD")
        
        if addon_settings.active:
            layout.label(text="Maintenance", icon="MODIFIER")
            box=layout.box()
            box.operator("objprop.clean_prop")
            

class OBJPROP_PT_Settings(MainPanel, bpy.types.Panel):
    bl_idname = "OBJPROP_PT_SETTINGS"
    bl_label = "Addon Settings"
    
    @classmethod
    def poll(self,context):
        return context.object is not None
    
    def draw(self, context):
        
        layout = self.layout
        scene = context.scene
        settings = scene.ObjProp_settings
        
        layout.label(text="General", icon="PREFERENCES")
        box=layout.box()
        box.prop(settings,"active")
        box.prop(settings,"description")
        box.prop(settings,"visibility_filter")
        row = box.row()
        row.prop(settings,"debug")
        row.prop(settings,"debug_verbose",text="Verbosity")
        
        layout.label(text="Maintenance", icon="MODIFIER")
        box=layout.box()
        box.operator("objprop.clean_prop", text="Reset all menus").active = False

# ------------------------------------------------------------------------
#    Menu Panel
# ------------------------------------------------------------------------

class MenuPanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    if bpy.context.scene.ObjProp_settings.active:
        bl_category = bpy.context.object.ObjProp_menu.name
    else:
        bl_category = bpy.context.scene.ObjProp_settings.global_name
    
class OBJPROP_PT_MenuPanel(MenuPanel, bpy.types.Panel):
    bl_idname = "OBJPROP_PT_MenuPanel"
    bl_label = "Object Properties"
    
    @classmethod
    def poll(self,context):
        
        scene = context.scene
        settings = scene.ObjProp_settings
        
        return settings.active
    
    def draw(self, context):
        
        obj = context.object
        
        layout = self.layout
        scene = context.scene
        settings = obj.ObjProp_menu
        
        if settings.show_obj_name:
            layout.label(text=obj.name, icon = obj.type+"_DATA")
        
        if ObjProp_CollectionPropFunctions.len_collection(obj.ObjProp_properties)>0:
            
            for el in obj.ObjProp_properties:
                if el.type == "OBJECT":
                    box=layout.box()
                    box.label(text="General", icon="SETTINGS")
                    break
            
            for el in obj.ObjProp_properties:
                if el.type == "OBJECT":
                    row = box.row(align=True)
                    row.label(text=el.name)
                    row.scale_x=settings.row_scale
                    row.prop(obj,el.identifier,text="")
            
            if obj.type=="MESH":
                for mat in obj.data.materials:
                    
                    for el in obj.ObjProp_properties:
                        if el.type == "MATERIAL" and el.type_identifier == mat.name:
                            box=layout.box()
                            box.label(text=mat.name, icon="MATERIAL")
                            break
                    
                    for el in obj.ObjProp_properties:
                        if el.type == "MATERIAL" and el.type_identifier == mat.name:
                            row = box.row(align=True)
                            row.label(text=el.name)
                            row.scale_x=settings.row_scale
                            row.prop(bpy.data.materials[el.type_identifier],el.identifier,text="")
            
            if obj.type=="LIGHT":
                for el in obj.ObjProp_properties:
                    if el.type == "LIGHT":
                        box=layout.box()
                        box.label(text="Light", icon="SETTINGS")
                        break
            
                for el in obj.ObjProp_properties:
                    if el.type == "LIGHT":
                        row = box.row(align=True)
                        row.label(text=el.name)
                        row.scale_x=settings.row_scale
                        row.prop(bpy.data.lights[obj.name],el.identifier,text="")
            
        else:
            box=layout.box()
            box.label(text="No properties set.",icon="ERROR")

class OBJPROP_PT_MenuPanelNoActive(MenuPanel, bpy.types.Panel):
    bl_idname = "OBJPROP_PT_MenuPanelNoActive"
    bl_label = "Object Properties"
    
    @classmethod
    def poll(self,context):
        
        scene = context.scene
        settings = scene.ObjProp_settings
        
        return not settings.active
    
    def draw(self, context):
        
        layout = self.layout
        scene = context.scene
        addon_settings = scene.ObjProp_settings
        
        check=False                    
        for obj in bpy.data.objects:
            settings = obj.ObjProp_menu
            if ObjProp_CollectionPropFunctions.len_collection(obj.ObjProp_properties)>0 and settings.show_no_active:
                check=True
        if not check:
            box = layout.box()
            box.label(text="No Object selected", icon="ERROR")
        
        for obj in bpy.data.objects:
            
            settings = obj.ObjProp_menu
            
            if ObjProp_CollectionPropFunctions.len_collection(obj.ObjProp_properties)>0 and settings.show_no_active:
        
                layout.label(text=obj.name, icon = obj.type+"_DATA")
                    
                for el in obj.ObjProp_properties:
                    if el.type == "OBJECT":
                        box=layout.box()
                        box.label(text="General", icon="SETTINGS")
                        break
                
                for el in obj.ObjProp_properties:
                    if el.type == "OBJECT":
                        row = box.row(align=True)
                        row.label(text=el.name)
                        row.scale_x=settings.row_scale
                        row.prop(obj,el.identifier,text="")
                
                if obj.type=="MESH":
                    for mat in obj.data.materials:
                        
                        for el in obj.ObjProp_properties:
                            if el.type == "MATERIAL" and el.type_identifier == mat.name:
                                box=layout.box()
                                box.label(text=mat.name, icon="MATERIAL")
                                break
                        
                        for el in obj.ObjProp_properties:
                            if el.type == "MATERIAL" and el.type_identifier == mat.name:
                                row = box.row(align=True)
                                row.label(text=el.name)
                                row.scale_x=settings.row_scale
                                row.prop(bpy.data.materials[el.type_identifier],el.identifier,text="")
                
                if obj.type=="LIGHT":
                    for el in obj.ObjProp_properties:
                        if el.type == "LIGHT":
                            box=layout.box()
                            box.label(text="Light", icon="SETTINGS")
                            break
                
                    for el in obj.ObjProp_properties:
                        if el.type == "LIGHT":
                            row = box.row(align=True)
                            row.label(text=el.name)
                            row.scale_x=settings.row_scale
                            row.prop(bpy.data.lights[obj.name],el.identifier,text="")
            

# ------------------------------------------------------------------------
#    Register/unregister classes
# ------------------------------------------------------------------------

classes = (
    OBJPROP_OT_AddProperty,
    OBJPROP_OT_RemoveProperty,
    OBJPROP_OT_MoveProperty,
    OBJPROP_OT_DescriptionProperty,
    OBJPROP_OT_CleanProperty,
    OBJPROP_PT_List,
    OBJPROP_PT_List_General,
    OBJPROP_PT_List_Materials,
    OBJPROP_PT_List_Lights,
    OBJPROP_PT_MenuSettings,
    OBJPROP_PT_Settings,
    OBJPROP_PT_MenuPanel,
    OBJPROP_PT_MenuPanelNoActive
)

def register():
    from bpy.utils import register_class
    
    for cls in classes:
        register_class(cls)

def unregister():
    
    from bpy.utils import unregister_class
    
    for cls in reversed(classes):
        unregister_class(cls)
        
    del bpy.types.Object.ObjProp_settings
    del bpy.types.Object.ObjProp_menus
    del bpy.types.Object.ObjProp_properties

if __name__ == "__main__":
    register()