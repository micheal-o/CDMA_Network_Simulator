#!/usr/bin/env python

"""main program for simulation"""
import basestation as bs #basestation class
import mobile as mb #mobile station class
import metrics_calc as metrics #for pl, shadowing, rsl, sinr, fading, eirp

#program initialization
print("initializing...")
prog_duration= 7200.0 #program duration in seconds
cell_box_list = metrics.shadowing()
bstn= bs.basestation() #create basestation object
for i in range(0,bstn.total_users):
    #create all mobiles
    bstn.mobiles_inactv.append(mb.mobile())
print_timer= 0 #timer for printing
program_timer= 0 #timer for program
print("Total num. of users:",bstn.total_users,"Cd:",bstn.c_d,"Ci:",bstn.c_i)

#runs every second
print("simulating...")
while(program_timer < prog_duration): 
    #checking all mobiles with active call
    for mobl in bstn.mobiles_actv:
        mobl.call_timer +=1
        if mobl.call_timer == mobl.call_duration:#call duration is complete
            bstn.end_call(mobl)
        else:#call still on
            mobl.rsl= metrics.rsl_dbm(bstn.eirp,bstn.c_freq,bstn.height,mobl.distance,mobl.shad_value)
            mobl.sinr = metrics.sinr(mobl.rsl,bstn.proc_gain,bstn.call_progress)
            bstn.ongoing_call(mobl) #also checks sinr re-attempts
            
    #checking all mobiles with inactive call
    for mobl in bstn.mobiles_inactv:
        if mobl.reattempt_rsl_count > 0: #mobile re-attempting a call
            mobl.rsl= metrics.rsl_dbm(bstn.eirp_pilot,bstn.c_freq,bstn.height,mobl.distance,mobl.shad_value)
            bstn.new_call(mobl) #re-attempt is also deactivated here once its 3
        elif mobl.is_call_attempt():
            #attempting a new call (initial attempt)
            mobl.set_location(bstn.radius) #set mobile coordinate (x,y)
            mobl.set_box(bstn.radius) #set the square in which mobile coordinate is located
            #in the 2D cell_box_list, 0-999 represent +ve axis for boxes
            #1000-1999 represent -ve axis for boxes, so we can represent it as
            #cell_box_list[box x axis][box y axis] to get shadowing value
            box_x,box_y= 0,0
            if mobl.box[0] < 0: #box is in -ve x axis
                box_x= 1000 + (abs(mobl.box[0])-1)
            else: #box is in +ve x axis
                box_x= mobl.box[0] - 1
            
            if mobl.box[1] < 0: #box is in -ve y axis
                box_y= 1000 + (abs(mobl.box[1])-1)
            else: #box is in +ve y axis
                box_y= mobl.box[1] - 1
                
            mobl.shad_value= cell_box_list[box_x][box_y]
            mobl.rsl= metrics.rsl_dbm(bstn.eirp_pilot,bstn.c_freq,bstn.height,mobl.distance,mobl.shad_value)
            bstn.new_call(mobl)
        else:
            #not attempting a call
            pass

    #admission control    
    bstn.admission_ctrl()
    #print statistics
    print_timer +=1 #increment statistics print timer
    program_timer +=1 #increment program timer
    if print_timer == 120: #print every 2 minutes
        print("Simulation statistics after %d seconds..." %(program_timer))
        bstn.print_stat()
        print_timer= 0
        if program_timer < prog_duration:
            print("simulating...")    
print("simulation completed")
#end of program
