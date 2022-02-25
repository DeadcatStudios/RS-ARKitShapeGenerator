import bpy

bl_info = {
    "name": "RoyalSkies Shape Generator",
    "author": "Deadcat", # i guess
    "version": (1, 0, 0),
    "blender": (3, 00, 1),
    "description": "Generate a Pose list and shape keys from it",
    "category": "RoyalSkies",
    }


shapelist = [
# ARKit
"eyeBlinkLeft",
"eyeLookDownLeft",
"eyeLookInLeft",
"eyeLookOutLeft",
"eyeLookUpLeft",
"eyeSquintLeft",
"eyeWideLeft",
"eyeBlinkRight",
"eyeLookDownRight",
"eyeLookInRight",
"eyeLookOutRight",
"eyeLookUpRight",
"eyeSquintRight",
"eyeWideRight",
"jawForward",
"jawLeft",
"jawRight",
"jawOpen",
"mouthClose",
"mouthFunnel",
"mouthPucker",
"mouthRight",
"mouthLeft",
"mouthSmileLeft",
"mouthSmileRight",
"mouthFrownRight",
"mouthFrownLeft",
"mouthDimpleLeft",
"mouthDimpleRight",
"mouthStretchLeft",
"mouthStretchRight",
"mouthRollLower",
"mouthRollUpper",
"mouthShrugLower",
"mouthShrugUpper",
"mouthPressLeft",
"mouthPressRight",
"mouthLowerDownLeft",
"mouthLowerDownRight",
"mouthUpperUpLeft",
"mouthUpperUpRight",
"browDownLeft",
"browDownRight",
"browInnerUp",
"browOuterUpLeft",
"browOuterUpRight",
"cheekPuff",
"cheekSquintLeft",
"cheekSquintRight",
"noseSneerLeft",
"noseSneerRight",
"tongueOut",
]

################################################################
########################## Operators ###########################
################################################################

class RS_GenerateShapeKeys(bpy.types.Operator):
    bl_idname = "rs.generate_shape_keys"
    bl_label = "Generate Shape keys"
    
    def execute(self, context):        
        global shapelist
        
        for obj in bpy.context.selected_objects:
            
            # if the object a mesh, dont wana be adding shape keys to armatures ;)
            if obj.type == 'MESH':
                # check if the objects have a any shape key, if not then add "Basis" (rest position)
                if not obj.data.shape_keys:
                    obj.shape_key_add(from_mix=False)
                    bpy.context.object.data.shape_keys.key_blocks[-1].name = 'Basis'
                #----------------------------------------------#
                             
                # for each shapename lets generate,  "i" will return the index so we can use it as the frame
                for i in range(len(shapelist)):
                    # the array will start at 0 so +1 for frame? 
                    # set the frame
                    bpy.context.scene.frame_set(i+1)
                    
                    
                    ## overide shape keys if it already exist ##
                    # check if existing shapekey exists
                    sh=obj.data.shape_keys.key_blocks.get(shapelist[i])
                    # Delete old shape to replace it with new 
                    if sh:
                        obj.shape_key_remove(sh)
                    #----------------------------------------------#
                    
                    # Just in case, lets set all current shape keys to 0, no double dipping
                    for sh in obj.data.shape_keys.key_blocks:
                        sh.value=0.0
                     
                    # Save As Shape_key
                    bpy.ops.object.modifier_apply_as_shapekey(keep_modifier=True, modifier="Armature")

                    # name the shape_key, get -1 will give us the last index in the array
                    bpy.context.object.data.shape_keys.key_blocks[-1].name = shapelist[i]
                    #----------------------------------------------#          
        return {'FINISHED'} 



# This op creates a action on the rig, then adds pose markers to that action to be filled out               
class RS_Generateposelib(bpy.types.Operator):
    bl_idname = "rs.generate_pose_lib"
    bl_label = "Generate Pose List"
    
    def execute(self, context):
        global shapelist
        
        arm = bpy.context.object
        # create the action(if it doesnt already exist), name it armature name+"ARKit_PL" in case there are multiple rigs in the scene
        act = bpy.data.actions.get(arm.name+"_ARKit_PL")
        
        if not act:
            act = bpy.data.actions.new(arm.name+"_ARKit_PL")
            
        if not arm.animation_data:
            arm.animation_data_create()
            print('Create')
            
        arm.animation_data.action=act
        
        # add a pose marker to every frame and name it after the shape so we can go through the list n not miss any :)
        for i in range(len(shapelist)):
            pm = act.pose_markers.get(shapelist[i])
            if not pm:
                pm = act.pose_markers.new(name=shapelist[i])
                pm.frame=i+1
                
        return {'FINISHED'}  
        
##################################################################
############################## UI ################################
################################################################## 

class SHAPEGENERATOR_PT_Panel(bpy.types.Panel):
    bl_label = "Face Shape Generator"
    bl_idname = "SHAPEGENERATOR_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Item"
    
    def draw(self, context):
        layout = self.layout 
        b = layout.box()
        col = b.column(align=True)
        if bpy.context.object.type!='ARMATURE':
            col.operator("rs.generate_shape_keys")
            
        else:
            col.operator("rs.generate_pose_lib")
            
            

classes = [
    RS_GenerateShapeKeys,
    RS_Generateposelib,
    SHAPEGENERATOR_PT_Panel
    ] 
    
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
        
if __name__ == "__main__":
    register()                  