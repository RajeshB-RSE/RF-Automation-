"""
=========================================================
config.py

Project Configuration

=========================================================
"""
import CMW
import config
import DUT
import time
import FSW

# -------------------------------------------------------
# CMW500
# -------------------------------------------------------

CMW_IP = "TCPIP0::192.168.0.5::inst0::INSTR"

FSW_IP = "TCPIP0::192.168.0.3::inst0::INSTR"

CMW_RESOURCE = "TCPIP0::192.168.0.5::inst0::INSTR"

FSW_RESOURCE = "TCPIP0::192.168.0.3::inst0::INSTR"

TIMEOUT = 30000

# -------------------------------------------------------
# GSM Test Configuration
# -------------------------------------------------------

BAND = "G19"

CHANNEL = 810

PATHLOSS = 42

PHONE_NUMBER = "112"

CALL_DURATION = 20

# -------------------------------------------------------
# DUT
# -------------------------------------------------------

PORT = 1          # A=0 B=1 C=2 D=3

MIN_BATTERY = 30

# -------------------------------------------------------
# Command Files
# -------------------------------------------------------

ONE_TIME_SETUP = "commands/one_time_setup.txt"

GSM_CONNECT = "commands/gsm_connect.txt"

# -------------------------------------------------------
# Logging
# -------------------------------------------------------

LOG_FOLDER = "logs"

RESULT_FOLDER = "results"


import config

cmw = CMW500(config.CMW_RESOURCE)

#dut.battery_check(config.MIN_BATTERY)

cmw.setup_gsm(
    config.BAND,
    config.CHANNEL,
    config.PATHLOSS
)

dut.execute_command_file(
    config.GSM_CONNECT,
    {"PORT": config.PORT}
)

dut.place_call(config.PHONE_NUMBER)

time.sleep(config.CALL_DURATION)

