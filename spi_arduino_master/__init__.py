"""
=========
spi_arduino_master
=========

spi_arduino_master model template The System Development Kit
Used as a template for all TheSyDeKick Entities.

Current docstring documentation style is Numpy
https://numpydoc.readthedocs.io/en/latest/format.html

This text here is to remind you that documentation is important.
However, youu may find it out the even the documentation of this 
entity may be outdated and incomplete. Regardless of that, every day 
and in every way we are getting better and better :).

Initially written by Marko Kosunen, marko.kosunen@aalto.fi, 2017.

"""

import os
import sys
#if not (os.path.abspath('../../thesdk') in sys.path):
#    sys.path.append(os.path.abspath('../../thesdk'))

#from thesdk import *
#from rtl import *
#from spice import *

import numpy as np
from serial import *
import time
import pdb



#class spi_arduino_master(thesdk):
class spi_arduino_master():
    @property
    def _classfile(self):
        return os.path.dirname(os.path.realpath(__file__)) + "/"+__name__

    def __init__(self,*arg): 
        #self.print_log(type='I', msg='Inititalizing %s' %(__name__)) 
        self.proplist = [ 'Rs' ];    # Properties that can be propagated from parent
        self.Rs =  100e6;            # Sampling frequency
        #self.IOS=Bundle()
        #self.IOS.Members['sclk']=IO() # Pointer for input data
        #self.IOS.Members['cs']=IO() # Pointer for input data:w
        #self.IOS.Members['miso']=IO()       # Pointer for input data
        #self.IOS.Members['mosi']=IO()       # Pointer for input data
        #self.IOS.Members['time']=IO()       # Pointer for input data

        self.read_from = "IOs"   # IOs or file. IOs not tested
        self.read_from = "file"   # IOs or file. IOs not tested
        self.file_in_path = 'in1.txt' 
        self.file_out_path = 'out1.txt' 
        
        self.model='py';             # Can be set externally, but is not propagated
        self.par= False              # By default, no parallel processing
        self.queue= []               # By default, no parallel processing
        #Collects mosi, cs and sclk controlled by master
        #self.IOS.Members['control_write']= IO() 
        #This is a placeholder, file is created by controller
        #_=rtl_iofile(self,name='control_write', dir='in', iotype='event', ionames=['reset', 'initdone', 'io_cs', 'io_mosi', 'io_sclk'])
        self.arduino = Serial('/dev/ttyACM0',baudrate=115200)
        print(self.arduino.name)
        time.sleep(0.1) 
        if len(arg)>=1:
            parent=arg[0]
            self.copy_propval(parent,self.proplist)
            self.parent =parent;

        self.init()

    def init(self):
        pass
        ### Lets fix this later on
        #if self.model=='vhdl':
        #    self.print_log(type='F', msg='VHDL simulation is not supported with v1.2\n Use v1.1')
    def write_read(self,x):
            d=self.arduino.write(bytes(x, 'utf-8'))
            #d=arduino.write(x)
            #time.sleep(0.001)
            data = self.arduino.read(size=1)
            return data

    def main(self):
        
        
        const_time=False
        time_step=1
        time_step_fact=10**(-1) 
                
        #print(arduino.readline())
        #time.sleep(0.1)
        if self.read_from=='file':
            first_line=True
            prev_time=0
            with open('in1.txt') as f, open('out1.txt', 'w') as f2:
                start_time=time.time_ns()
            
                for line in f:
                    #pdb.set_trace()
                    if const_time==False:
                        time_step=int(line.strip().split(' ')[0])-prev_time
                    prev_time=int(line.strip().split(' ')[0])
                    data=str(int(("".join(line.strip().split(' ')[1:4])),2))
                    time.sleep(time_step*time_step_fact)
                    #num = input("Enter a number: ") # Taking input from user
                    #if int(num) ==int(5):
                    #    
                    time_r1=time.time_ns()
                    value = self.write_read(data).strip()
                    time_r2=time.time_ns()
                    print('Writetime='+str((time_r2-time_r1)/ (10 ** 9)))
                    print(value) # printing the valueerial
                    f2.write(str(prev_time)+' '+str(int(value))+'\n')
                stoptime=time.time_ns()
                print((stoptime-start_time)/ (10 ** 9))
        elif self.read_from=='IOs':
            #t=self.IOS.Members['time'].Data
            #cs=self.IOS.Members['cs'].Data
            #sclk=self.IOS.Members['sclk'].Data
            #mosi=self.IOS.Members['mosi'].Data
            #miso=np.zeros(len(t))
            #pdb.set_trace() 
            t=np.arange(22).reshape(-1,1)
            cs=np.zeros_like(t)
            cs[len(t)-1]=1
            sclk=np.zeros_like(t)
            sclk[np.arange(len(t))[1::2]]=1
            mosi=np.zeros_like(t)
            mosi[np.array([4,5,6,7,12,13,14,15,19,20,21])]=1
            miso=np.zeros(len(t))

            start_time=time.time_ns()
            prev_time=0
            data=(np.hstack((sclk,mosi,cs)))# .astype(str)
            data_in=data.dot(2**np.arange(3)[::-1]).astype(str)
            #data_in=np.char.add(data[:,0],data[:,1])
            #data_in=np.char.add(data_in,data[:,2])
            for i in range(len(data_in)):

                #pdb.set_trace()
                if const_time==False:
                    time_step=t[i][0]-prev_time
                prev_time=t[i][0]
                data=data_in[i]
                time.sleep(time_step*time_step_fact)
                #num = input("Enter a number: ") # Taking input from user
                #if int(num) ==int(5):
                #    
                time_r1=time.time_ns()
                value = self.write_read(data).strip()
                time_r2=time.time_ns()
                print('Writetime='+str((time_r2-time_r1)/ (10 ** 9)))
                print(value) # printing the valueerial
                miso[i]=value
            stoptime=time.time_ns()
            print((stoptime-start_time)/ (10 ** 9))

            pdb.set_trace()
            #self.IOS.Members['miso'].Data=miso
            a=5
    def run(self,*arg):
        if len(arg)>0:
            self.par=True      #flag for parallel processing
            self.queue=arg[0]  #multiprocessing.queue as the first argument
        if self.model=='py':
            self.main()
        
    def define_io_conditions(self):
        # Input A is read to verilog simulation after 'initdone' is set to 1 by controller
        self.iofile_bundle.Members['sclk'].verilog_io_condition='initdone'
        self.iofile_bundle.Members['miso'].verilog_io_condition='initdone'
        self.iofile_bundle.Members['mosi'].verilog_io_condition='initdone'
        self.iofile_bundle.Members['time'].verilog_io_condition='initdone'
        self.iofile_bundle.Members['cs'].verilog_io_condition='initdone'
        # Output is read to verilog simulation when all of the utputs are valid, 
        # and after 'initdo' is set to 1 by controller
        #self.iofile_bundle.Members['cs'].verilog_io_condition_append(cond='&& initdone')
        # In Cpol0 Cpha1 miso is read with falling edge of sclk
        #self.iofile_bundle.Members['miso'].verilog_io_sync='@(negedge io_sclk)\n'
        #self.iofile_bundle.Members['miso'].verilog_io_condition_append(cond='&& initdone')


if __name__=="__main__":
    #import matplotlib.pyplot as plt
    #from  spi_arduino_master import *
    #from  spi_arduino_master.controller import controller as spi_controller
    import pdb
    

    duts=[spi_arduino_master() ]
    #pdb.set_trace()
    for d in duts: 
        d.run()

