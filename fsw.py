import time
import pyvisa

FSW_IP = "TCPIP0::192.168.0.3::inst0::INSTR"


class FSW:

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

        self.inst = self.rm.open_resource(self.resource)

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
    def setup_instruments(self):

        self.write('*RST')
        self.write("*CLS")
        self.query('*OPC?')
        self.write('MMEM:LOAD:STAT 1,"C:/R_S/instr/user/colocation/BT-GSM.dfl"')
        self.query('*OPC?')
        self.write(f'DISP:WIND:TRAC1:MODE WRIT')
        self.write(f'DISP:WIND:TRAC2:MODE WRIT')
        self.write(f'DISP:WIND:TRAC3:MODE WRIT')
        self.write(f'DISP:WIND:TRAC4:MODE WRIT')
        #self.sleep(1)
        self.write('DISP:WIND:TRAC1:MODE MAXH')
        self.write('DISP:WIND:TRAC2:MODE AVER')
        self.write('DISP:WIND:TRAC3:MODE WRIT')
        self.write('DISP:WIND:TRAC4:MODE MAXH')
        self.query("*OPC?")

    def wait_measurement(self, seconds=5):

        print("Waiting for acquisition...")

        time.sleep(seconds)

    def mark_peaks(self, markers=3, seconds=3):

        # Highest Peak
        time.sleep(seconds)
        self.write("CALC:MARK1:MAX")

        time.sleep(seconds)
        for i in range(2, markers + 1):
            time.sleep(1)
            self.write(f"CALC:MARK{i}:STAT ON")
            time.sleep(2)
            self.write(f"CALC:MARK{i}:NEXT")
