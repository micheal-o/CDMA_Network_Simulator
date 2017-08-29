#!/usr/bin/env python

"""basestation module
This module contains the class definition for the base station in the cell"""

import mobile

class basestation(object):
    "Class for creating a base station object in the cell"
    def __init__(self):
        "constructor"
        self.height= 50 #base station height (meters)
        self.radius= 10.0 #base station radius (km)
        self.max_tx_pow= 42 #maximium transmitter power (dBm)
        self.lc_loss= 2.1 #line and connector losses (dB)
        self.ant_gain= 12.1 #antenna gain (dB)
        self.eirp= self.max_tx_pow + self.ant_gain - self.lc_loss #eirp of communication channels (dBm)
        self.min_pilot_eirp= 30 #lower bound on the eirp of the pilot (dBm)
        self.c_freq= 1900 #carrier frequency (MHz)
        self.traff_ch= 56 #total number of traffic channels
        self.free_traff_ch= 56 #number of available traffic channels
        self.req_sinr= 6 #required SINR (dB)
        self.min_pl_rsl= -107 #minimium pilot RSL (dBm)
        self.total_users= 10000 #total number of users
        self.call_attempts= 0 #number of call attempts excluding retries
        self.call_attempts_re= 0 #number of call attempts including retries
        self.dropped= 0 #number of dropped calls
        self.blckd_sigstren= 0 #number of blocked calls due to signal strength
        self.blckd_cap= 0 #number of blocked calls due to channel capacity
        self.call_success= 0 #number of successfully completed calls
        self.call_progress= 0 #number of calls in progress at a given time
        self.call_failed= 0 #number of failed calls (blocks + drops)
        self.c_d= 20 #20 number of channels in use for pilot EIRP to decrease
        self.c_i= 15 #15 number of channels in use for pilot EIRP to increase
        self.mobiles_actv= [] #list of mobiles with active call
        self.mobiles_inactv= [] #list of mobiles with inactive call
        self.eirp_pilot= self.eirp #EIRP of the pilot (dBm)
        self.delta_eirp_pilot= 0.5 #change in EIRP for admission control (dB)
        self.proc_gain = 20 #processor gain (dB)

    def admission_ctrl(self):
        "Handles the admission control mechanism"
        if (self.traff_ch - self.free_traff_ch) > self.c_d: #decrease pilot EIRP
            if self.eirp_pilot == self.min_pilot_eirp:
                #minimium eirp reached
                pass
            else:
                self.eirp_pilot -= self.delta_eirp_pilot
        elif (self.traff_ch - self.free_traff_ch) < self.c_i: #increase pilot EIRP
            if self.eirp_pilot == self.eirp:
                #maximium eirp reached
                pass
            else:
                self.eirp_pilot += self.delta_eirp_pilot
        else:
            pass
        return

    def new_call(self, mobl):
        "Handles all call attempts by mobiles without ongoing call"
        self.call_attempts_re += 1 #call attempts including retries
        if mobl.reattempt_rsl_count == 0: #call attempts excluding retries
            self.call_attempts += 1
        if mobl.rsl >= self.min_pl_rsl: #adequate pilot RSL
            mobl.reattempt_rsl_count = 0
            if self.free_traff_ch > 0: #traffic channel is available
                mobl.call_status= "active"
                mobl.set_call_duration()
                mobl.call_timer= 0
                self.free_traff_ch -= 1
                self.call_progress += 1
                self.mobiles_actv.append(mobl)
                self.mobiles_inactv.remove(mobl)
                return
            else: #traffic channel is unavailable 
                mobl.call_status= "inactive"
                self.blckd_cap += 1
                self.call_failed += 1
                return
        else: #inadequate pilot RSL
            if mobl.reattempt_rsl_count == 2: #3 consecutive reattempts completed
                mobl.reattempt_rsl_count = 0
                self.blckd_sigstren += 1
                self.call_failed += 1
            else: #less than 3 consecutive reattempts completed
                mobl.reattempt_rsl_count += 1
            return

    def ongoing_call(self, mobl):
        "Monitors mobiles with ongoing call"
        if mobl.sinr >= self.req_sinr: #sufficient SINR
            mobl.reattempt_sinr_count = 0
            return
        else: #insufficient SINR
            if mobl.reattempt_sinr_count == 2: #3 consecutive reattempts completed
                mobl.reattempt_sinr_count= 0
                mobl.call_status= "inactive"
                mobl.call_duration= 0
                mobl.call_timer= 0
                self.free_traff_ch += 1
                self.dropped += 1
                self.call_failed += 1
                self.call_progress -= 1
                self.mobiles_actv.remove(mobl)
                self.mobiles_inactv.append(mobl)
            else: #less than 3 consecutive reattempts completed
                mobl.reattempt_sinr_count += 1
            return
    
    def end_call(self, mobl):
        "Terminates a completed call"
        mobl.call_status= "inactive"
        mobl.call_duration= 0
        mobl.call_timer= 0
        self.free_traff_ch += 1
        self.call_success += 1
        self.call_progress -= 1
        self.mobiles_actv.remove(mobl)
        self.mobiles_inactv.append(mobl)
        return

    def cell_radius(self):
        "get the current cell radius in Km"
        max_distance= 0.0
        for mobl in self.mobiles_actv: #list of mobiles with active call
            if mobl.distance > max_distance:
                max_distance= mobl.distance
        return max_distance
    
    def print_stat(self):
        "print basestation statistics"
        print("Num. of call attempts not counting retries:",self.call_attempts)
        print("Num. of call attempts including retries:",self.call_attempts_re)
        print("Num. of dropped calls:",self.dropped)
        print("Num. of blocked calls due to signal strength:",self.blckd_sigstren)
        print("Num. of blocked calls due to channel capacity:",self.blckd_cap)
        print("Num. of successfully completed calls:",self.call_success)
        print("Num. of calls in progress (now):",self.call_progress)
        print("Num. of failed calls (blocks + drops):",self.call_failed)
        print("Current cell radius(Km):",self.cell_radius())
        print("\n")
        return
