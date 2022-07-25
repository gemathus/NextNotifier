from re import A, S
from blink1.blink1 import Blink1, blink1
import os
from constants.apps import APPS
class Blink:
    def __init__(self):
        self.blink1 = Blink1()
        self.free_ports = [1,2]
        self.port_state = {1: "", 2: ""}

        #check if state.bl file exists
        if os.path.exists('state.bl'):
            with open('state.bl', 'r') as f:
                self.state = f.read().split(",")
                self.port_state[1] = self.state[0].split(":")[1]
                self.port_state[2] = self.state[1].split(":")[1]
                if self.port_state[1] != "":
                    self.blink1.fade_to_color(0,self.port_state[1],1)
                if self.port_state[2] != "":
                    self.blink1.fade_to_color(0,self.port_state[2],2)
                f.close()
        else:
            self.blink1.off()
            
    def shutdown(self):
        self.blink1.off()

    def turn_off(self, led):
        self.blink1.fade_to_color(0, 'black', led)
        self.port_state[led] = ""
    
    def turn_on(self, led, color):
        if led == 0:
            if self.port_state[1] != color:
                self.blink1.fade_to_color(0, color)
            if self.port_state[2] != color:
                self.blink1.fade_to_color(0, color)
            self.set_port_state(1, color)
            self.set_port_state(2, color)
            return
        if self.port_state[led] != color:
            self.blink1.fade_to_color(0, color, led)
            self.port_state[led] = color
            self.set_port_state(led, color)

    def notify(self, app_names):
        for app_name in app_names:
            if app_name not in APPS.keys():
                print("returning")
                self.shutdown()
                return

        app_colors = [APPS[app]["color"] for app in app_names]
        if self.port_state[1] != "" and self.port_state[1] not in app_colors:
            self.turn_off(1)
        if self.port_state[2] != "" and self.port_state[2] not in app_colors:
            self.turn_off(2)
        
        if len(app_names) > 2:
            self.turn_on(0, "red")
            return
        
        if len(app_names) == 1:
            self.turn_on(0, APPS[app_names[0]]["color"])
            return

        if len(app_names) == 2:
            app_0_color = APPS[app_names[0]]["color"]
            app_1_color = APPS[app_names[1]]["color"]
            if app_0_color != self.port_state[1] and app_0_color != self.port_state[2]:
                self.turn_on(1, app_0_color)
            if app_1_color != self.port_state[1] and app_1_color != self.port_state[2]:
                self.turn_on(2, app_1_color)
            return

    
    def set_port_state(self, port, color):
        self.port_state[port] = color
        self.write_state()
    
    def write_state(self):
        with open('state.bl', 'w+') as f:
            state = "1:{},2:{}".format(self.port_state[1], self.port_state[2])
            f.write(state)
            