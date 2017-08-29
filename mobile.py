#!/usr/bin/env python

"""mobile module
This module contains the class definition for all mobiles in the cell"""

import numpy as np
import math

class mobile(object):
    "Class for creating a mobile station object in the cell"
    avg_call_duration= 1.0 #average call duration for all mobiles in minutes
    def __init__(self):
        "constructor"
        self.call_status= "inactive" #status of call, active|inactive
        self.reattempt_sinr_count= 0 #number of consecutive reattempts due to SINR
        self.reattempt_rsl_count= 0 #number of consecutive reattempts due to RSL
        self.call_duration= 0 #requested call duration in seconds
        self.call_timer= 0 #current call duration in seconds
        self.location= (0,0) #coordinate (x,y)
        self.distance= 0 #distance to basestation in km
        self.box= (0,0) #coordinate (x,y) of the square the mobile is located
        self.rsl= 0 #RSL at a particular time
        self.sinr= 0 #SINR for a call at a particular time
        self.shad_value= 0 #shadowing value of the current mobile location

    def is_call_attempt(self):
        "Mobile should make a call or not, with a prob. of 6/3600 = 1/600"
        result= np.random.randint(1,601)
        #a random integer (1-600) using a discrete uniform distribution
        #with equal probability of occurrence
        if result == 600:
            return 1 #make call
        else:
            return 0 #don't make call

    def set_location(self, cell_radius):
        "set the location of a mobile in the cell"
        self.distance= 0.0
        while self.distance <= 0.0 or self.distance > cell_radius:
            #there are 20,000 points on x axis, 1 meter distance between consecutive points
            x= np.random.randint(-10000,10001,None)
            #there are 20,000 points on y axis, 1 meter distance between consecutive points
            y= np.random.randint(-10000,10001,None)
            #the above make sure every point in the cell has equal probability
            #of occurrence
            self.location= (x,y)
            self.distance= math.sqrt(math.pow(x,2) + math.pow(y,2))/1000
        return

    def set_box(self, cell_radius):
        "set the box/square the mobile station is located"
        box_x,box_y= 0,0
        #-ve axis for boxes are labelled, -1 - -1000
        #+ve axis for boxes are labelled, 1 - 1000
        if self.location[0] < 0: #mobile is on -ve x axis
            if abs(self.location[0]) == cell_radius * 1000:
                box_x= -1000
            else:
                box_x= 0 - (math.floor(abs(self.location[0])/10) + 1)
        else: #mobile on +ve x axis
            if self.location[0] == 0:
                box_x= 1
            elif self.location[0] == cell_radius * 1000:
                box_x= 1000
            else:
                box_x= math.floor(self.location[0]/10) + 1

        if self.location[1] < 0: #mobile is on -ve y axis
            if abs(self.location[1]) == cell_radius * 1000:
                box_y= -1000
            else:
                box_y= 0 - (math.floor(abs(self.location[1])/10) + 1)
        else: #mobile on +ve y axis
            if self.location[1] == 0:
                box_y= 1
            elif self.location[1] == cell_radius * 1000:
                box_y= 1000
            else:
                box_y= math.floor(self.location[1]/10) + 1
        self.box= (box_x,box_y)
        return
        
    def set_call_duration(self):
        "set the call duration for a mobile object in seconds"
        self.call_duration= np.random.exponential(mobile.avg_call_duration,None)
        #call duration in seconds
        self.call_duration *= 60
        self.call_duration = round(self.call_duration)
        return
    
