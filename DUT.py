import time
import re
import logging
import pexpect
import sys

class DUTController:

    PROMPT = r":-\)"
    min_percent = 30
    def __init__(self):
        self.session = None

    def __init__(self, nkdp):
        """
        nkdp = pexpect.spawn object
        """
        self.nkdp = nkdp

    def __init__(self,
             nanokdp_cmd="nanokdp",
             timeout=120):
        self.timeout = timeout
        self.nkdp = pexpect.spawn(
            nanokdp_cmd,
            encoding="utf-8",
            timeout=timeout
        )
        self.nkdp.logfile_read = None
        print("NanoKDP Started")

    ####################################################################
    # DUT CONNECT
    ####################################################################
    def connect(self):
        print("\nStarting nanokdp...\n")

        self.session = pexpect.spawn(
            "nanokdp",
            encoding="utf-8",
            timeout=60
        )

        # Uncomment for debugging
        self.session.logfile = sys.stdout

    def select_device(self):

        print("\nWaiting for device list...\n")

        try:
            # Give nanokdp time to print devices
            self.session.expect(
                [
                    "Select",
                    "select",
                    "Device",
                    "device"
                ],
                timeout=15
            )

            output = self.session.before + self.session.after

            print("\nAvailable Devices:\n")
            print(output)

        except pexpect.TIMEOUT:
            print("Unable to detect device list.")
            sys.exit(1)

        device_no = input(
            "\nEnter Device Number: "
        ).strip()

        print(f"\nConnecting to DUT {device_no}...\n")

        # Select DUT
        self.session.sendline(device_no)

        # Nanokdp requires additional ENTER
        self.session.sendline("")

        self.wait_for_diag_prompt()

    def wait_for_diag_prompt(self):

        print("Waiting for diagnostic prompt :-)\n")

        try:
            self.session.expect(
                self.PROMPT,
                timeout=30
            )

            print("\nDUT Connected Successfully\n")

        except pexpect.TIMEOUT:
            print(
                "\nTimeout waiting for DUT diagnostic prompt :-)"
            )
            sys.exit(1)
    ####################################################################
    # Generic command execution
    ####################################################################

    def execute_command(self, command, timeout=30):

        #logging.info(f"CMD : {command}")

        #self.nkdp.sendline(command)

        #self.nkdp.expect(":-)", timeout=timeout)

        #output = self.nkdp.before.decode(errors="ignore")

        #logging.info(output)

        #return output

        print(f"\n>>> {command}")

        self.session.sendline(command)

        try:

            self.session.expect(
                self.PROMPT,
                timeout=120
            )

            response = self.session.before.strip()

            print("\nResponse:")
            print("--------------------------------")
            print(response)
            print("--------------------------------")

            return response

        except pexpect.TIMEOUT:

            print(
                f"\nTimeout waiting for completion of: {command}"
            )

            return ""

    ####################################################################
    # Wait for Prompt
    ####################################################################

    def wait_for_prompt(self, timeout=120):

        print("Waiting for NanoKDP prompt...")

        self.nkdp.expect(":-)", timeout=timeout)

        print("Prompt Ready")

        return True

    ####################################################################
    # Reset DUT
    ####################################################################

    def reset(self):

        print("Resetting DUT...")

        self.execute_command("reset")

        print("Waiting DUT reboot...")

        self.wait_for_prompt(180)

        print("Reset Complete")

    ####################################################################
    # Battery Check
    ####################################################################

    def battery_check(self):

        response = self.execute_command(
            "device -k gasgauge -p"
        )

        match = re.search(
            r'(\d+)\s*%',
            response
        )

        if match:
            battery = match.group(1)
            print(
                f"\nBattery Percentage: {battery}%"
            )
            return battery

        print(
            "\nBattery percentage not found."
        )

        return None


        raise Exception("Cannot read battery level")

    ####################################################################
    # Baseband Version
    ####################################################################

    def get_baseband_version(self):

        rsp = self.execute_command("baseband --on --load")

        print(rsp)

        return rsp

    ####################################################################
    # Set Antenna Port
    ####################################################################

    def set_antenna_port(self, port):

        cmd = (
            f'baseband --send '
            f'"at@rfsw:rfSetAntennaPort_at({port})"'
        )

        rsp = self.execute_command(cmd)

        return rsp

    ####################################################################
    # Read Antenna Port
    ####################################################################
    def get_antenna_port(self):

        rsp = self.execute_command(
            'baseband --send '
            '"at@rfsw:rfGetAntennaPort_at(0)"'
        )

        print(rsp)

        return rsp

    ####################################################################
    # Wait Network Registration
    ####################################################################

    def wait_for_network_registration(self,
                                      timeout=120):

        print("Waiting GSM Registration...")

        start = time.time()

        while True:

            rsp = self.execute_command(
                'baseband --send "at+cereg?"'
            )

            if ("0,1" in rsp or
                "0,5" in rsp):

                print("Registered")

                return True

            if time.time() - start > timeout:

                raise TimeoutError(
                    "Network Registration Timeout"
                )

            time.sleep(2)

    ####################################################################
    # Place Call
    ####################################################################

    def place_call(self,
                   number="112"):

        print(f"Dialing {number}")

        rsp = self.execute_command(
            f'baseband --send "ATD{number};"',
            timeout=60
        )

        return rsp
    ####################################################################
    # Hang Up
    ####################################################################
    def hangup(self):

        print("Hangup")

        rsp = self.execute_command(
            'baseband --send "ATH"'
        )

        return rsp
    ####################################################################
    # Execute Command File
    ####################################################################
    def execute_command_file(self,
                             filename,
                             variables=None):

        variables = variables or {}

        with open(filename) as f:

            for line in f:

                line = line.strip()

                if not line:

                    continue

                if line.startswith("#"):

                    continue

                for key, value in variables.items():

                    line = line.replace(
                        "${"+key+"}",
                        str(value)
                    )

                if line.upper().startswith("WAIT"):

                    ms = int(line.split()[1])

                    time.sleep(ms/1000)

                    continue

                self.execute_command(line)

                if line.lower() == "reset":

                    #self.wait_for_prompt()
                    pass