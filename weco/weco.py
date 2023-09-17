#link to video:
#https://youtu.be/pbn0ndpo37U
import bpy
import random
from math import radians, sin , cos , pi

#restart
#bpy.ops.object.select_all(action = "SELECT")
#bpy.ops.object.delete()

shape = bpy.ops
modifier = bpy.ops.object.modifier_add

#create cube shape
def cube(loc, random_size, random_degrees):
    shape.mesh.primitive_cube_add(
        size = random_size * random.random(),
        enter_editmode = False,
        align = "WORLD",
        location = loc,
        scale = (1, 1, 1)
        )
    #modifiers to create cool things
    modifier(type = "WAVE")
    modifier(type = "SIMPLE_DEFORM")
    bpy.context.object.modifiers["SimpleDeform"].angle = radians(random_degrees * random.random())
    modifier(type = "WIREFRAME")
    bpy.context.object.modifiers["Wireframe"].thickness = 0.1
    #color-note that with select_all and delete, it will also delete the materials:
    if random.random() <= 0.5:
        bpy.context.object.data.materials.append(bpy.data.materials["Material.001"])
    else:
        bpy.context.object.data.materials.append(bpy.data.materials["Material.003"]) 
    
#create curve shape
def curve(loc,z_size):
    shape.curve.primitive_bezier_curve_add(
        radius = 1, 
        enter_editmode = False,
        align = "WORLD",
        location = loc,
        scale = (35, 1, z_size)
        )
    bpy.context.object.rotation_euler[1] = radians(-90)
    #scale-did this to allow finer control
    bpy.context.object.scale[0] = 7
    bpy.context.object.scale[1] = -0.1
    bpy.context.object.scale[2] = 0.1
    #location
    bpy.context.object.location[2] = 25
    #modifiers
    shape.object.convert(target="MESH")
    modifier(type = "WAVE")
    modifier(type="SKIN")
    #subsurf
    modifier(type = "SUBSURF")
    bpy.context.object.modifiers["Subdivision"].levels = 2
    bpy.context.object.modifiers["Subdivision"].render_levels = 3
    modifier(type="WIREFRAME")  
    if random.random() <= 0.5:
        bpy.context.object.data.materials.append(bpy.data.materials["Material.002"]) 
    else:
        bpy.context.object.data.materials.append(bpy.data.materials["Material.004"])   

#taken from the provided github
def setAnimation(o,o_x,o_y, o_z_scale):
    frame_number = 0

    for i in range(100):
        
        # Set the current frame
        bpy.context.scene.frame_set(frame_number)  
        
        z = sin(i+o_y+o_x*0.2)
        
        o.location = (o_x+cos(i)+3, o_y+cos(i)+3, 15)
        o.scale = (15,0.2, +o_z_scale+sin(i+o_y*0.1-0.4))

        o.keyframe_insert(data_path='location', index=-1)
        o.keyframe_insert(data_path='scale', index=-1)

        frame_number += 15

#taken and edited from the first lesson with blender
#used to create multiple cubes
random_size = 2
random_degrees = 0
if random.random() >= 0.5:
    random_degrees = 90
else: 
    random_degrees = -90
for x in range(5):
    for y in range(5):
        for z in range(11):
            cube((x*3, y*3, z*3), random_size, random_degrees)
            item = bpy.context.object
            frame_number = 0
            for k in range(100):
                bpy.context.scene.frame_set(frame_number)
                item.location = ((x*3 + cos(k), y*3, z*3 + sin(k)))
                item.keyframe_insert(data_path = "location", index =- 1)
                frame_number += 5


#taken from the example provided on the website
X = 2
Y = 2
for x in range(4):
    for y in range(4):
        z_size = 1*random.random()
        Z = 1*random.random()
        curve((x*X, y*Y, 0), Z)
        item = bpy.context.object
        setAnimation(item, x*X, y*Y, Z)       
        
        
        
        
#taken and smashed in from this video by CG COOKIE 
#https://www.youtube.com/watch?v=QnvN1dieIAU       
all_shapes = bpy.data.collections["Collection"].objects
offset = 0
for x in all_shapes:
    x.scale = (0,0,0)
    x.keyframe_insert(data_path = "scale", frame = 1 + offset)
    x.scale = (1,1,5)
    x.keyframe_insert(data_path = "scale", frame = 50 + offset)
    x.scale = (1,1,5)
    x.keyframe_insert(data_path = "scale", frame = 70 + offset)
    x.scale = (1,1,1)
    x.keyframe_insert(data_path = "scale", frame = 100 + offset)
    offset += 1


#frame ends  
bpy.context.scene.frame_end = 500


#took a while to figured out how to rotate around the object
default_cube = bpy.ops.object.empty_add(
    type='CUBE', 
    align='WORLD', 
    location=(5.5159, 5.7916, 14.888), 
    scale=(1, 1, 1)
    )
current_scene = bpy.context.scene    
cameraPath = bpy.context.active_object
cameraPath.keyframe_insert("rotation_euler", frame=1)
bpy.context.object.rotation_euler[2] = radians(360)
cameraPath.keyframe_insert("rotation_euler", frame=500)


#camera
bpy.ops.object.camera_add(
    enter_editmode=False, 
    align='VIEW', 
    location=(0.14, 133.5, 19.1), 
    rotation=(radians(82), radians(0), radians(-180)), 
    scale=(1, 1, 1)
    )

#link them together
#learn from:
#https://blender.stackexchange.com/questions/9200/how-to-make-object-a-a-parent-of-object-b-via-blenders-python-api
#https://www.youtube.com/watch?v=Y9odlxWL_pI&t=26s
objects = bpy.data.objects
a = objects['Empty']
b = objects['Camera']
b.parent = a


