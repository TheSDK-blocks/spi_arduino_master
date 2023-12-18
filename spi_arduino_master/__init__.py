"""
===================
spi_arduino_master
===================

SPI master with Arduino. Has 2 implementations/structures:

1: Compatible with SDK spi_slave controller generated files. Outputs of spli_slave controller can be connected to the input IOs. This entity will go once trhough the IO files and write them to Arduino's pins and retur miso. Aclso can be se to read and write to txt files by setting self.read_from to "file" instead of "IOs". Entity is used by self.run() function. One values/line is red from IOs/file and written straight to Arduino's pins and miso ir read.

2: Do not requires of running self.run() function but instead is used by 2 separate functions: writeToMem(self,conf), pushConf(self,conf). 

In Arduino swithc between structure is done by commenting and uncommenting corresponding parts.

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
        self.structure=2 # 1, 2

        self.const_time=False
        self.time_step=1
        self.time_step_fact=10**(-1)       
        
        self.model='py';             # Can be set externally, but is not propagated
        self.par= False              # By default, no parallel processing
        self.queue= []               # By default, no parallel processing
        #Collects mosi, cs and sclk controlled by master
        #self.IOS.Members['control_write']= IO() 
        #This is a placeholder, file is created by controller
        #_=rtl_iofile(self,name='control_write', dir='in', iotype='event', ionames=['reset', 'initdone', 'io_cs', 'io_mosi', 'io_sclk'])
        self.arduino = Serial('/dev/ttyACM0',baudrate=9600)
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
        """
        Functions takes string of an integer that represets value of sclk, mosi and cs and updates given values to Arduino's pins while reading and returning miso pin.

        Parameters
        -----------
            x : string
                string of integer,  "4"
        """
        d=self.arduino.write(bytes(x, 'utf-8'))
        d=arduino.write(x)
        time.sleep(0.001)
        data = self.arduino.read(size=1)
        return data



    def writeToMem(self,conf):
        """
            Functions takes binary string (big endian) as a "conf" parameter and writes that configure string to Arduino's memory.

            Parameters
            -----------
            conf : string
                binary string (big endian),  "010101101"
        """
        
        #pdb.set_trace()
        conf_len=len(conf)
        bytes_num=int(np.ceil(len(conf)/8))
        conf_array=[0]*(bytes_num)
        #conf_array[0]='w'
        z=''.join(map(str,np.zeros(bytes_num*8-conf_len).astype(int)))
        conf= z+conf
        conf=conf[::-1]
        #d=self.arduino.write(bytes('w', 'utf-8'))
        for i in range(0,bytes_num):
            #pdb.set_trace()
            test=conf[8*i:8*(i+1)]
            data=str(int(conf[8*i:8*(i+1)],2))
            print(test)
            print(data)
            conf_array[i]=int(data)
            #conf_array[i]=''.join([chr(int(test,2))])

        #pdb.set_trace()
        w=bytes('w', 'utf-8')
        self.arduino.write(w)
        self.arduino.flush()
        for x in conf_array:
            
            a=self.arduino.write(x.to_bytes(1,'big'))
            self.arduino.flush()
            #self.arduino.flush()
            time.sleep(0.1)
            #self.arduino.flush()
        #    self.arduino.write(x.encode())  # Send the 20-bit string to Arduino
        #    self.arduino.flush()
        #    pdb.set_trace()
        #self.arduino.write(conf_array)  # Send the 20-bit string to Arduino
        self.arduino.flush()
        #pdb.set_trace()
        time.sleep(1)
        #pdb.set_trace()
        print(self.arduino.in_waiting)
        if self.arduino.in_waiting==0:
            print("For some reason sometimes writing fails, try again. Sorry")
            exit()

        while 1:
            if self.arduino.in_waiting>0:
                print(self.arduino.read(1))
            else:
                break
        #d=self.arduino.write(bytes(conf_array))
        #d=self.arduino.write(bytes(conf_array, 'utf-8'))

        a=5

    def pushConf(self,conf):
        """
         Function pushed configure string from Arduino's memory to pins and reads miso intput to memory. After whole configure string is sent to pins, miso string is returned from Arduino to return valuae of the function. This function requires same configure string as a "conf" parameter as writeToMem(self,conf) in order to know the expected number of bytes.

         Parameters
         ----------
         conf : string
            binary string (big endian),  "010101101"


        """
        conf_len=len(conf)
        bytes_num=int(np.ceil(len(conf)/8))
        mon_array=np.zeros(bytes_num)
        n=bytes('n', 'utf-8')
        self.arduino.reset_input_buffer()
        self.arduino.write(b'p')
        self.arduino.flush()
        #pdb.set_trace()

        while 1:
            if self.arduino.in_waiting>1:
                #pdb.set_trace()
                test=self.arduino.read(1)
                print(test)
                if test.decode()=='a':
                    #self.arduino.read(2)
                    break

                 

        i=0
        while 1:
            if self.arduino.in_waiting>0:
                val=self.arduino.read(1)
                mon_array[i]=int.from_bytes(val,'big')
                self.arduino.write(n)
                i=i+1

            if i==bytes_num:
                break

        #x= self.arduino.read(size=3)
        #y=''.join(format(byte,'08b') for byte in x)


        #d=self.arduino.write(bytes('p', 'utf-8'))

        #mon_array = self.arduino.read(size=bytes_num)
        monitor=''
        for x in mon_array:
            monitor=monitor+np.binary_repr(int(x),8)
        monitor=monitor[::-1]
        self.arduino.reset_input_buffer()
        pdb.set_trace()
        a=5
        return monitor

    def main(self):
        if self.structure ==1: 
            const_time=self.const_time
            time_step=self.time_step
            time_step_fact=self. time_step_fact                 
            #pdb.set_trace() 
            #print(arduino.readline())
            #time.sleep(0.1)
            if self.read_from=='file':
                first_line=True
                prev_time=0
                with open('in1.txt') as f, open('out1.txt', 'w') as f2:
                    start_time=time.time_ns()
                
                    for line in f:
                        pdb.set_trace()
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
                # Inputs

                #t=self.IOS.Members['time'].Data
                #cs=self.IOS.Members['cs'].Data
                #sclk=self.IOS.Members['sclk'].Data
                #mosi=self.IOS.Members['mosi'].Data
                #miso=np.zeros(len(t))
                #pdb.set_trace() 

                # Test values
                t=np.arange(22).reshape(-1,1)
                cs=np.zeros_like(t)
                cs[len(t)-1]=1
                sclk=np.zeros_like(t)
                sclk[np.arange(len(t))[1::2]]=1
                mosi=np.zeros_like(t)
                mosi[np.array([4,5,6,7,12,13,14,15,19,20,21])]=1
                miso=np.zeros(len(t))


                # Function starts
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
        elif self.structure==2:
            #pdb.set_trace()
            conf_len=20
            bytes_num=int(np.ceil(conf_len/8))
            conf_array=np.zeros(bytes_num)
            mon_array=np.zeros(bytes_num)
            conf=np.zeros(conf_len)
            #conf[::2]=1
            conf=''.join(map(str,conf.astype(int)))
            conf='101000000000000000011111111'
            #z=''.join(map(str,np.zeros(bytes_num*8-conf_len).astype(int)))
            #conf= z+conf
            self.writeToMem(conf)
            time.sleep(1)
            monitor=self.pushConf(conf)
            print(monitor[len(monitor)-len(conf):]==conf)



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

