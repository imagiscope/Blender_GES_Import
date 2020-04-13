import bpy, json, mathutils, math, bmesh
from mathutils import *

cam = bpy.context.scene.camera

scene = bpy.context.scene
# load the GES render files as background for camera
# Sample format: ifiles = "D:/Local/Project/Beach/beach/footage/beach_0000.jpeg"
ifiles = "D:/Local/Project/sydney/sydney/footage/sydney_000.jpeg"

img = bpy.data.movieclips.load(ifiles)
cam.data.show_background_images = True
bg = cam.data.background_images.new()
bg.clip = img
bg.alpha = 1
bg.source = "MOVIE_CLIP"

# load JSON file for evaluation
# Sample format: jfilename = "D:/Local/Project/Beach/beach/beach.json"
jfilename = "D:/Local/Project/sydney/sydney/sydney.json"

jfile = open(jfilename,'r')
camdata = json.load(jfile)
jfile.close

# evaluate number of frames
s_end = camdata["numFrames"]

# set scene duration
scene.frame_start = 0
scene.frame_end = s_end 
scene.frame_set(0)

# function for alignment scaling
def scale_from_vector(v):
    mat = Matrix.Identity(4)
    for i in range(3):
        mat[i][i] = v[i]
    return mat   
        
# set coords for positioning data starting at center of Blender global coordinates
psx = 0
psy = 0
psz = 0 

# load trackpoints
for f in range (0,len(camdata["trackPoints"])):
    
    px = camdata["trackPoints"][f]["position"]["x"]
    py = camdata["trackPoints"][f]["position"]["y"]
    pz = camdata["trackPoints"][f]["position"]["z"]
    
    rlat = camdata["trackPoints"][f]["coordinate"]["position"]["attributes"][0]["value"]["relative"]
    rlng = camdata["trackPoints"][f]["coordinate"]["position"]["attributes"][1]["value"]["relative"]
    
    if f==0:
        psx = px
        psy = py
        psz = pz
        
    rlat = 360 * (rlat) - 180
    rlng = 180 * (rlng ) - 90
    
    bpy.ops.mesh.primitive_plane_add()
    trk = bpy.context.selected_objects[0]
    trk.name = camdata["trackPoints"][f]["name"]
  
    trk.location.x = (px-psx) / 100
    trk.location.y = (py-psy) / 100
    trk.location.z = (pz-psz) / 100
    
    trk.rotation_euler[1] = math.radians(90-rlng)
    trk.rotation_euler[2] = math.radians(rlat)
    trk.scale = (0.1,0.1,0.1)
    
    if f==0:
        # create parent object - parent used to align position on earth with Blender global coordinates
        bpy.ops.object.empty_add(type='SINGLE_ARROW', location=(0,0,0))
        ges_parent = bpy.context.selected_objects[0]
        ges_parent.name = "_GES_WORLD"
        
        # align parent perpendicular to first track point
        loc_src, rot_src, scale_src = trk.matrix_world.decompose()
        loc_dst, rot_dst, scale_dst = ges_parent.matrix_world.decompose()

        axis = Vector((0.0, 0.0, 1.0))
        z1 = rot_src @ axis
        z2 = rot_dst @ axis
        q = z2.rotation_difference(z1)

        ges_parent.matrix_world = (
            Matrix.Translation(loc_dst) @
            (q @ rot_dst).to_matrix().to_4x4() @
            scale_from_vector(scale_dst)
        )
        
        # change x,y to negative values of x,y
        ges_parent.rotation_euler[0] = -ges_parent.rotation_euler[0]
        ges_parent.rotation_euler[1] = -ges_parent.rotation_euler[1]
              
    # move trackpoint to GES parent
    trk.parent = ges_parent
 

# Camera Information
cam.delta_rotation_euler.y = 180 * math.pi / 180

for f in range (0,s_end + 1):
    px = camdata["cameraFrames"][f]["position"]["x"] 
    py = camdata["cameraFrames"][f]["position"]["y"] 
    pz = camdata["cameraFrames"][f]["position"]["z"] 
   
        
    rx = float(camdata["cameraFrames"][f]["rotation"]["x"])
    ry = camdata["cameraFrames"][f]["rotation"]["y"] 
    rz = camdata["cameraFrames"][f]["rotation"]["z"]
    
    # position set in relation to first frame - scale to 1/100
    cam.location.x = (px-psx) / 100
    cam.location.y = (py-psy) / 100
    cam.location.z = (pz-psz) / 100
 
    eul = mathutils.Euler((0.0, 0.0, 0.0), 'XYZ')
    
    eul.rotate_axis('X', math.radians(-rx))
    eul.rotate_axis('Y', math.radians(ry ))
    eul.rotate_axis('Z', math.radians(-rz+180))
    
    cam.rotation_euler = eul
  
    cam.keyframe_insert(data_path="location", index=-1, frame=f)
    cam.keyframe_insert(data_path="rotation_euler", index=-1, frame=f)
    
    
# camera "lens" based on 20 degree Filed of View (default value)
cam.data.sensor_width = 35 
cam.data.type = 'PERSP'
cam.data.lens_unit = 'FOV'
cam.data.angle = math.radians(34.8)

# move camera to GES parent
cam.parent = ges_parent

bpy.context.scene.frame_current = 0

print("done")

    
    