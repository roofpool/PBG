##Packed-Bed generation module (Version-Beta)
##BPartopour, AG Dixon†
##Heat and Mass Transfer Lab
##Worcester Polytechnic Institute

#Rigid-body generator module
import bpy
import bmesh
import math 
import random
import parameters
import numpy as np
import logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


x=[]
y=[]
z=[]
# generates five objects every time it is  called
# choosing a random location to drop from in i range, close to top of cylinder
def part_generation(pellet_key,x_y_range,phi_range,top,vectors):
    PARTS = 5
    from Rashig_ring import Rashig_ring
    #from fpoint_star import fpoint_star
    #from three_holes import three_holes_generator
    #from fh import four_hole_generator
    #from tri_lobes import tri_lobes_generator
    #from quadrilobes import quadrilobes_generator
    #from spheres_fh import sphere_4holes_generator

    if len(x_y_range) < PARTS:
        pop_2 = list(np.arange(-1,1,0.3))
        x = random.sample(pop_2,PARTS)
        y = random.sample(pop_2,PARTS)
    else: 
        x = random.sample(x_y_range, PARTS)
        y = random.sample(x_y_range, PARTS)
    z = random.sample(range(top, top + 8),PARTS)
    x_r = random.sample(phi_range, PARTS)
    y_r = random.sample(phi_range, PARTS)
    z_r = random.sample(phi_range, PARTS) 


    for i in range(PARTS):
        
        if pellet_key == 0:
            logging.info(f"part_generation generating spheres: {i+1}/{PARTS}.")
            print(f"generating {i+1}/{PARTS} spheres")
            bpy.ops.mesh.primitive_uv_sphere_add(segments=28, 
                                                 ring_count=28, 
                                                 radius = parameters.particle_radius, 
                                                 location = (x[i],y[i],z[i]))
        elif pellet_key == 9:
            logging.info(f"part_generation generating irregular particles: {i+1}/{PARTS}.")
            print(f"generating {i+1}/{PARTS} particles")
            stl_particle_001 = bpy.ops.wm.stl_import(filepath=r"C:\Users\h93p771\OneDrive - Montana State University\Documents\GitHub\PBG\Scale_up_stl_particle_001.stl")
            #for use on linux machine (./whatever_name)
            #stl_particle_001 = bpy.ops.wm.stl_import(filepath=r"./Scale_up_stl_particle_001.stl")

            obj = bpy.context.active_object
                        
            # Set the location (X, Y, Z)
            obj.location = (x[i],y[i],z[i])
                                             
        elif pellet_key == 1:
            bpy.ops.mesh.primitive_cylinder_add(vertices = 50,
                                                end_fill_type = 'TRIFAN',
                                                radius = parameters.particle_radius,
                                                depth = parameters.particle_length,
                                                location = (x[i], y[i],z[i]),
                                                rotation = (x_r[i], y_r[i], z_r[i]))
        elif pellet_key == 2:
            Rashig_ring(outer_radius = parameters.particle_radius,
                        inner_radius = parameters.particle_inner_radius,
                        depth = parameters.particle_length,
                        location = (x[i], y[i], z[i]),
                        rotation = (x_r[i], y_r[i], z_r[i]))
                        #elif pellet_key == 3:
                        #            fpoint_star()
                        #
                        #        elif pellet_key == 4:
                        #            four_hole_generator(vectors, x,y,z,x_r,y_r,z_r,i)
                        #        elif pellet_key == 5:
                        #            three_holes_generator(vectors, x, y,z,x_r,y_r,z_r,i,radi = parameters.particle_radius)
                        #       elif pellet_key == 6:
                        #           tri_lobes_generator(parameters.particle_length, x, y, z, x_r, y_r, z_r,i)
                        #       elif pellet_key == 7:
                        #           quadrilobes_generator(parameters.particle_length, x, y, z, x_r, y_r, z_r,i)
                        #       elif pellet_key == 8:
                        #           sphere_4holes_generator(x,y,z,x_r,y_r,z_r,i)
        bpy.ops.rigidbody.objects_add(type='ACTIVE')
        obj = bpy.context.object.rigid_body
        obj.enabled = True
        obj.collision_shape = parameters.collision_shape
        #obj.mass = 1
        obj.friction = parameters.friction_factor
        obj.restitution = parameters.restitution_factor
        obj.mesh_source = 'BASE'
        obj.use_margin = parameters.use_margin
        obj.collision_margin = parameters.collision_margin
        obj.linear_damping = parameters.linear_damping
        obj.angular_damping = parameters.rotational_damping

def tube_generation(cyl_radius, cyl_depth):

    cyl_vertices = 100
    bpy.ops.mesh.primitive_cylinder_add(location = (0,0,0),
                                        vertices = cyl_vertices,
                                        radius = cyl_radius,
                                        depth = cyl_depth)
    obj = bpy.ops.object
    obj.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_all(action = 'TOGGLE')

    obj = bpy.context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    if hasattr(bm.verts, "ensure_lookup_table"):
        bm.faces.ensure_lookup_table()
    bm.faces[(cyl_vertices-2)].select = True
    bpy.ops.mesh.delete(type = 'FACE')
    obj_new = bpy.ops.object
    obj_new.mode_set(mode = 'OBJECT')
    obj_new.modifier_add( type = 'SOLIDIFY')
    bpy.context.object.modifiers["Solidify"].thickness  = 0.02
    obj_new.modifier_apply( modifier = "Solidify")
    bpy.ops.rigidbody.object_add(type = 'PASSIVE')
    obj = bpy.context.object.rigid_body
    obj.collision_shape = 'MESH'
    obj.friction = 0.1
    obj.restitution = 0.1
    obj.use_margin = parameters.use_margin
    obj.collision_margin = parameters.collision_margin
    
    #activating split impulse

    bpy.context.scene.rigidbody_world.enabled = True
    bpy.context.scene.rigidbody_world.use_split_impulse = True
    bpy.context.scene.rigidbody_world.substeps_per_frame = 200
    bpy.context.scene.rigidbody_world.solver_iterations = 200
    bpy.context.scene.gravity = (0.0, 0.0, -20.0)
