'''
    This Tango Class device server is for the NewPort AG_UC8 Controller
    
    It uses the qcodes_contrib_drivers basics functions
    
    https://qcodes.github.io/Qcodes_contrib_drivers/examples/Newport_AG-UC8.html

'''


import time
import json
import qcodes
from qcodes_contrib_drivers.drivers.Newport.AG_UC8 import Newport_AG_UC8

import tango
from tango import AttrQuality, AttrWriteType, DevState, DispLevel, AttReqType, Database
from tango.server import Device, attribute, command
from tango.server import class_property, device_property


import Thorlabs_Python_Code.DMP40_ctypes

class AG_UC8(Device):
    AG_UC8_Device = {}

    host = device_property(dtype=str, default_value="localhost")
    port = class_property(dtype=int, default_value=10000)


    def init_device(self):
        super().init_device()
        self.info_stream(f"Connection details: {self.host}:{self.port}")
        self.set_state(DevState.ON)
        self.set_status("Thorlabs CAMS Driver is ON, you need to connect a camera")


    def delete_device(self):
        return 



    '''
        AG_UC8 =        {
                            "Name"      : <user_name_given_on Connect>,
                            "COM"       : 0,
                        }
    '''    


    @command(dtype_in=str,dtype_out=str)  
    def Connect(self,AG_UC8):
        AG_UC8 =  json.loads(AG_UC8)
        print(AG_UC8)
        ctl = Newport_AG_UC8("Newport","ASRL"+str(AG_UC8["COM"]))
        
        print(self.AG_UC8_Device)
        self.AG_UC8_Device[AG_UC8["Name"]] = ctl

        return str(self.AG_UC8_Device[AG_UC8["Name"]].get_idn())
    


    def check_channel_and_axies(self,userinfo):
        if userinfo["Axis"] == 1:
            return self.AG_UC8_Device[userinfo["Name"]].channels[userinfo["Channel"]].axis1
        elif  userinfo["Axis"] == 2:
            return self.AG_UC8_Device[userinfo["Name"]].channels[userinfo["Channel"]].axis2
        else:
            return -1
        
        
    '''
        userinfoZP =   {
                            "Name"      : <user_name_given_on Connect>,
                            "Channel"   : 0 to 3,
                            "Axis"      : 1 or 2
                        }
    '''


    @command(dtype_in=str,dtype_out=str)  
    def ZeroPosition(self,userinfoZP):
        print("ZeroPosition")
        userinfoZP =  json.loads(userinfoZP)
        print(userinfoZP)
        helper =  self.check_channel_and_axies(userinfoZP)
        if helper == -1:
            return "Axis not correct"
        else:
            helper.zero_position()
        
        return "Channel "+ str(userinfoZP["Channel"])+ ", Axies "+ str(userinfoZP["Axis"] )+" was set to zero"
 


    '''
        userinfoMP =   {
                            "Name"      : <user_name_given_on Connect>,
                            "Channel"   : 0 to 3,
                            "Axis"      : 1 or 2
                        }
    '''       
    # The position is returned as a number from 0 to 1000 
    # corresponding to the full travel range of the mount.
    @command(dtype_in=str,dtype_out=str)  
    def MeasurePosition(self,userinfoMP):
        userinfoMP =  json.loads(userinfoMP)
        helper =  self.check_channel_and_axies(userinfoMP)
        if helper == -1:
            return "Axis not correct"
        else:
           return str(helper.measure_position())  

         
    
    '''
        userinfoMR =   {
                            "Name"      : <user_name_given_on Connect>,
                            "Channel"   : 0 to 3,
                            "Axis"      : 1 or 2,
                            "Position"  : 0 to 500
                        }
    '''   

    @command(dtype_in=str,dtype_out=str)  
    def MoveRel(self,userinfoMR):
        userinfoMR =  json.loads(userinfoMR)
        helper =  self.check_channel_and_axies(userinfoMR)
        if helper == -1:
            return "Axis not correct"
        else:
           helper.move_rel(userinfoMR["Position"])
           return " The motor is starting moving"
    
    '''
        userinfoS =   {
                            "Name"      : <user_name_given_on Connect>,
                            "Channel"   : 0 to 3,
                            "Axis"      : 1 or 2
                        }
    '''   


    @command(dtype_in=str,dtype_out=str)  
    def StatusMotor(self,userinfoS):
        print("StatusMotor")
        userinfoS =  json.loads(userinfoS)
        print(userinfoS)
        helper =  self.check_channel_and_axies(userinfoS)
        if helper == -1:
            return "Axis not correct"
        else:
           print(helper.status())
           return " Status: "+str(helper.status())
    

    '''
        userinfoR =   {
                            "Name"      : <user_name_given_on Connect>
                        }
    '''   

    @command(dtype_in=str,dtype_out=str)  
    def Reset(self,userinfoR):
        userinfoR =  json.loads(userinfoR)
        self.AG_UC8_Device[userinfoR["Name"]].reset()
        return "The controller was reseted"
        
    
    
    
    '''
        userinfoSAP =   {
                            "Name"      : <user_name_given_on Connect>,
                            "Channel"   : 0 to 3,
                            "Axis"      : 1 or 2
                        }
    '''   

    @command(dtype_in=str,dtype_out=str)  
    def StepAmplitudePos(self,userinfoSAP):
        userinfoSAP =  json.loads(userinfoSAP)
        helper =  self.check_channel_and_axies(userinfoSAP)
        if helper == -1:
            return "Axis not correct"
        else:
           return str(helper.step_amplitude_pos())
        

    '''
        userinfoSAN =   {
                            "Name"      : <user_name_given_on Connect>,
                            "Channel"   : 0 to 3,
                            "Axis"      : 1 or 2
                        }
    '''   

    @command(dtype_in=str,dtype_out=str)  
    def StepAmplitudeNeg(self,userinfoSAN):
        userinfoSAN =  json.loads(userinfoSAN)
        helper =  self.check_channel_and_axies(userinfoSAN)
        if helper == -1:
            return "Axis not correct"
        else:
           return str(helper.step_amplitude_neg())


    '''
        userinfoSteps =   {
                            "Name"      : <user_name_given_on Connect>,
                            "Channel"   : 0 to 3,
                            "Axis"      : 1 or 2
                        }
    '''   
    
    @command(dtype_in=str,dtype_out=str)  
    def Steps(self,userinfoSteps):
        print("Steps")
        userinfoSteps =  json.loads(userinfoSteps)
        print(userinfoSteps)
        helper =  self.check_channel_and_axies(userinfoSteps)
        if helper == -1:
            return "Axis not correct"
        else:
           return str(helper.steps())

        
if __name__ == "__main__":
    AG_UC8.run_server()
