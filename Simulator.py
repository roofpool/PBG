##Packed-Bed generation module (Version-BAeta)
##BPartopour, AG Dixon†
##Heat and Mass Transfer Lab
##Worcester Polytechnic Institute

#Simulator module

import bpy
import math
import parameters
import logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def rigidbody_simulation(Particle_type, last_particle_drop_frame):
    from Rigidbody_generator import part_generation
    import numpy as np
    
    co_max = 0.6*parameters.cyl_radius - parameters.particle_radius
    co_min = -1.0 * co_max
    #The current depth is 30, thus the answer to this is negative, is this a problem?
    top = round((parameters.cyl_depth/4) - 10)
    interval =  parameters.particle_radius
    x_y_range = list(np.arange(co_min,co_max,interval))
    phi_range = list(np.arange(0.0,6.28,0.5))
    pellet = {'sphere' : 0, 'cylinder' : 1, 'Raschig Ring':2, 'f_point_star':3, 
              'four_holes':4, 'three_holes':5, 'tri_lobes': 6, 'quadrilobes' : 7, 
              'four_hole_sphere' :8, 'stl_particle_001' :9}
    pellet_key = pellet[Particle_type]
    simulation_current_frame = 1
#    scene = bpy.context.scene
#    fp = scene.render.filepath

    if pellet_key == 4:
        from fh import four_holes_coor
        vectors = four_holes_coor()
    elif pellet_key == 5:
        from three_holes import three_holes_coor
        vectors = three_holes_coor()
    else:
        vectors=[]
        
    i = 0
    for i in range(last_particle_drop_frame):
        # generate 5 spheres every tenth frame
        if (simulation_current_frame % 10) == 0.0:
            part_generation(pellet_key,x_y_range,phi_range,top,vectors)
        
        bpy.context.scene.frame_set(frame = simulation_current_frame)
#        scene.render.filepath = fp + str(i+1)
#        bpy.ops.render.render(write_still=True)
        simulation_current_frame += 1
    return(simulation_current_frame)
    



def steady_state(simulation_current_frame):
    logging.info(f"steady_state called with {simulation_current_frame}.")
    size= len(bpy.context.selected_objects)
    x = [0]*size
    y = [0]*size
    z = [0]*size
    x_prev = [0]*size
    y_prev = [0]*size
    z_prev = [0]*size
    d = [1]*size
    Stop = False
 #   scene = bpy.context.scene
 #   fp = scene.render.filepath
 #   i = simulation_current_frame
    while ( Stop == False ):
       
        i = 0
        for obj in bpy.context.selected_objects:
            logging.info(f"steady_state i: {i} obj: {obj}.")
            current_obj = obj
            x[i],y[i],z[i] = obj.matrix_world.translation
            d[i]=(((((x[i]-x_prev[i])**2))+(((y[i]-y_prev[i])**2))+(((z[i]-z_prev[i])**2)))**0.5)
            x_prev[i],y_prev[i],z_prev[i] = x[i],y[i],z[i]
            i = i+1
        if max(d) < 0.5:
            logging.info(f"steady_state stopping max(d): {max(d)}.")
            Stop = True
            #note: the below is a kill switch for the code to prevent extensive run time for falling particles
            #change the max(d) value if the cylinder is long and there is chance of large distances in falling simulation 
        elif max(d) > 20 :
            logging.error(f"steady_state stopping due to escaped particle max(d): {max(d)}.")
            Stop = True
            print("A particle has escaped the tube and the simulation was terminated.")
        logging.info(f"steady_state continuing max(d): {max(d)}.")
        bpy.context.scene.frame_set(frame = simulation_current_frame)
#        scene.render.filepath = fp + str(simulation_current_frame)
#        bpy.ops.render.render(write_still=True)
        simulation_current_frame += 1
        logging.info(f"steady_state advancing frame: {simulation_current_frame}.")
    print(f"Last frame in steady state {simulation_current_frame}")
    return(d)

