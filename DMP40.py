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

class DMP40(Device):
    DMP40_Device = {}

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
        #   TODO 

        return "On working"
        
if __name__ == "__main__":
    DMP40.run_server()
