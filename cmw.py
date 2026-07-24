#!/usr/bin/env python3

"""
=====================================================

CMW500.py

PyVISA Driver

=====================================================
"""

import time
import pyvisa


class CMW:

    def __init__(self,
                 resource,
                 timeout=30000):

        self.resource = resource
        self.timeout = timeout

        self.rm = None

        self.inst = None

    ###################################################

    def connect(self):

        print("Opening VISA Resource...")

        self.rm = pyvisa.ResourceManager()
        self.inst = self.rm.open_resource('192.168.0.5::inst0::INSTR')

        self.inst.timeout = self.timeout

        self.inst.write_termination = '\n'

        self.inst.read_termination = '\n'

        print("Connected")

    ###################################################

    def disconnect(self):

        if self.inst:

            self.inst.close()

        if self.rm:

            self.rm.close()

    ###################################################

    def write(self, cmd):

        print(">>", cmd)

        self.inst.write(cmd)

    ###################################################

    def query(self, cmd):

        print(">>", cmd)

        rsp = self.inst.query(cmd)

        print("<<", rsp)

        return rsp

    ###################################################

    def idn(self):

        return self.query("*IDN?")

    ###################################################

    def reset(self):

        self.write("*RST")

        self.write("*CLS")

        time.sleep(2)

    ###################################################

    def setup_gsm(self,
                  band,
                  channel,
                  pathloss):

        print("Configure GSM")

        #
        # Replace these SCPI commands with
        # your validated CMW500 GSM signaling
        # commands.
        #

        self.write("*RST")

        self.write("*CLS")

        self.write(f"CONF:GSM")

        self.write(f"CONF:GSM:BAND {band}")

        self.write(f"CONF:GSM:CHAN {channel}")
        self.write(f"CONFigure:GSM:SIGN:RFSettings:CHANnel:TCH {channel}")
        self.write("CONFigure:GSM:SIGN:RFSettings:PMAX:BCCH 0")
        self.write("CONF:GSM:SIGN:RFS:CHAN:TCH?")
        self.write(f"CONFigure:GSM:SIGN:RFSettings:EATTenuation:INP {pathloss}")
        self.write(f"CONFigure:GSM:SIGN:RFSettings:EATTenuation:OUTP {pathloss}")
        self.write("CONF:GSM:SIGN:RFS:ENPM ULPC")
        self.write("CONF:GSM:SIGN:RFS:PCL:TCH:CSW 0")
        self.write("SOUR:GSM:SIGN1:CELL:STAT?")
        self.write("SOURce:GSM:SIGN1:CELL:STATe ON")
        #
        # RF Routing
        #

        self.write(f"CONF:GSM:RF:LOSS {pathloss}")

        time.sleep(2)

    ###################################################

    def cell_on(self):

        print("Cell ON")

        self.write("OUTP:GSM ON")

    ###################################################

    def cell_off(self):

        print("Cell OFF")

        self.write("OUTP:GSM OFF")

    ###################################################

    def registration_status(self):

        return self.query("FETC:GSM:SIGN:REG:STAT?")

    ###################################################

    def wait_registration(self,
                          timeout=120):

        print("Waiting Registration")

        start = time.time()

        while True:

            rsp = self.registration_status()

            if "REGISTERED" in rsp.upper():

                print("Registered")

                return True

            if time.time()-start > timeout:

                raise TimeoutError(
                    "Registration Timeout"
                )

            time.sleep(2)

    ###################################################

    def call_status(self):
        
        self.write("CALL:GSM:SIGN:CSWitched:ACTion CONNect")
        return self.query("FETC:GSM:SIGN:CSW:STAT?")
    ###################################################

    def wait_call_connected(self,
                            timeout=120):

        print("Waiting Call")

        start = time.time()

        while True:

            rsp = self.call_status()

            if "CEST" in rsp.upper():

                return True

            if time.time()-start > timeout:

                raise TimeoutError(
                    "Call Timeout"
                )

            time.sleep(1)

    ###################################################

    def current_power(self):

        return self.query("READ:GSM:MEAS:POW?")

    ###################################################

    def current_ber(self):

        return self.query("READ:GSM:MEAS:BER?")

    ###################################################

    def current_rssi(self):

        return self.query("READ:GSM:MEAS:RSSI?")