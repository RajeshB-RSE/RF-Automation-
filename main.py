#!/usr/bin/env python3
"""
==========================================================
RF Automation
main.py

Author  : Rajesh B
Platform: macOS
Python  : 3.10+

Workflow

1. Connect CMW500
2. Launch NanoKDP
3. Select DUT
4. Battery Check
5. Baseband Version
6. One-Time Setup
7. Reset DUT
8. GSM Call Setup
9. Configure CMW500
10. Wait Registration
11. Place Call
12. Verify Call
13. Hold Call
14. Hangup
15. Disable Cell

==========================================================
"""

import sys
import time
import traceback

from DUT import DUTController
from CMW500 import CMW500
from FSW import FSW

###############################################################
# USER CONFIGURATION
###############################################################

CMW_IP = "192.168.0.5"

BAND = "G19"

CHANNEL = 810

PORT = 2         # Port A=0 B=1 C=2 D=3

PATHLOSS = 42

CALL_DURATION = 20

PHONE_NUMBER = "112"

###############################################################


def banner():

    print("\n")
    print("=" * 60)
    print("        RF GSM AUTOMATION")
    print("=" * 60)
    print()


def main():

    banner()

    cmw = None
    dut = None

    try:

        ##########################################################
        # Connect CMW500
        ##########################################################

        print("\nConnecting CMW500...")

        cmw = CMW500(CMW_IP)

        cmw.connect()

        print(cmw.idn())


        ##########################################################
        # Start NanoKDP
        ##########################################################

        print("\nLaunching NanoKDP...")

        dut = DUTController()

        dut.connect()

        dut.select_device()

        dut.wait_for_prompt()


        ##########################################################
        # Battery Check
        ##########################################################

        print("\nBattery Check")

        dut.battery_check(30)


        ##########################################################
        # Baseband Version
        ##########################################################

        print("\nBaseband Version")

        dut.get_baseband_version()


        ##########################################################
        # One Time Setup
        ##########################################################

        print("\nRunning One-Time Setup")

        dut.execute_command_file(

            "/Users/rse/Documents/GSM_call_auto/one_time_setup.txt"

        )


        ##########################################################
        # Reset DUT
        ##########################################################

        #print("\nReset DUT")

        #dut.reset()


        ##########################################################
        # Configure GSM Cell
        ##########################################################

        print("\nConfigure CMW500")

        cmw.setup_gsm(

            band=BAND,

            channel=CHANNEL,

            pathloss=PATHLOSS

        )

        cmw.cell_on()
        fsw.connect()


        ##########################################################
        # GSM Connection Commands
        ##########################################################

        print("\nPrepare DUT")

        dut.execute_command_file(

            "/Users/rse/Documents/GSM_call_auto/gsm_connect.txt",

            {

                "PORT": PORT

            }

        )


        ##########################################################
        # Verify Antenna
        ##########################################################

        print("\nVerify Antenna")

        dut.get_antenna_port()


        ##########################################################
        # Registration
        ##########################################################

        #print("\nWaiting Registration")

        #dut.wait_for_network_registration()


        ##########################################################
        # Call
        ##########################################################

        #print("\nDial Call")

        #dut.place_call(PHONE_NUMBER)


        ##########################################################
        # Verify Call
        ##########################################################

        print("\nWaiting Call Connected")

        cmw.wait_call_connected()

        print("CALL CONNECTED")

        ##########################################################
        # BT Connection Commands
        ##########################################################

        print("\nPrepare BLE COMMANDS TO DUT")

        dut.execute_command_file("/Users/rse/Documents/GSM_call_auto/BLE_COMMAND_GSM.txt",

            {

                "PORT": PORT

            }

        )
        
        #print("\nInitiate FSW.......")

        fsw.setup_instruments()


        ##########################################################
        # Disable Cell
        ##########################################################

        cmw.cell_off()

        print("\nAutomation Completed Successfully")


    except KeyboardInterrupt:

        print("\nUser Interrupted")


    except Exception as e:

        print("\nAutomation Failed")

        print(e)

        traceback.print_exc()


    finally:

        print("\nCleaning Up")

        try:

            if dut:

                dut.disconnect()

        except:

            pass

        try:

            if cmw:

                cmw.disconnect()

        except:

            pass

        print("Done")


###############################################################

if __name__ == "__main__":

    main()