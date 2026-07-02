# RF Automation
## Overview

RF Automation is a Python-based automation tool developed to simplify RF validation activities by integrating communication between:

- DUT (via NanoKDP)
- Rohde & Schwarz CMW500
- Rohde & Schwarz FSW Spectrum Analyzer
- EMCenter

The objective is to automate GSM/LTE call establishment, RF measurements, screenshot capture, and report generation with minimal manual intervention.

---

## Features

### DUT Communication
- NanoKDP communication
- Automatic UART/KOBA device detection
- Manual device selection
- Execute single commands
- Execute command script files
- Reset DUT
- Battery status
- Baseband status

### CMW500
- Connect via VISA
- GSM Cell Configuration
- LTE Cell Configuration
- Wait for DUT Attach
- Call Establishment
- Call Release

### Spectrum Analyzer (FSW)
- Connect via VISA
- Basic Spectrum Measurement
- Marker Measurement
- Peak Search
- Screenshot Capture
- Trace Save

### EMCenter
- Instrument Control
- Start Test
- Stop Test

### Reporting
- Log Generation
- Screenshot Storage
- Excel Summary Report

---

# Project Structure

RF Automation

├── main.py

├── config.py

├── dut.py

├── cmw500.py

├── fsw.py

├── emcenter.py

├── scripts/

│ ├── gsm/

│ ├── lte/

│ └── common/

├── results/

│ ├── Logs/

│ ├── Screenshot/

│ └── Summary.xlsx

├── requirements.txt

└── README.md

---

## Installation

### Install Python Packages

```bash
pip3 install -r requirements.txt
```

---

## Verify Installation

```bash
python3 --version
```

Recommended Version

```
Python 3.11+
```

---

## Running

```bash
python3 main.py
```

---

## Workflow

### GSM

```
Connect DUT (UART)

↓

Reset DUT

↓

Run GSM One-Time Script

↓

Reconnect DUT (KOBA)

↓

Run Port Script

↓

Connect CMW500

↓

Configure GSM Cell

↓

Wait for DUT Attach

↓

Call Established

↓

Spectrum Measurement

↓

Save Screenshot

↓

Generate Excel Report
```

---

### LTE

```
Connect DUT

↓

Reset

↓

Run LTE Script

↓

Configure LTE Cell

↓

Wait for Attach

↓

Call Established

↓

Spectrum Measurement

↓

Save Screenshot

↓

Excel Report
```

---

## Scripts

DUT commands are stored separately under the scripts directory.

Example:

```
scripts/gsm/portB.txt
```

```
baseband --set bootargs "boot-mode=0"

WAIT 1000

baseband --on --load

WAIT 1000

baseband -p
```

Advantages

- No Python modification required
- Easy to update
- Version controlled
- Reusable

---

## Results

After execution

```
results/

Logs/

Screenshot/

Summary.xlsx
```

will be generated automatically.

---

## Future Enhancements

- LTE Automation
- NR (5G) Support
- Automatic Test Queue
- GUI
- Multiple DUT Support
- Automatic Report Generation
- XML/CSV Export
- Antenna Mast Automation

---

## Author

Rajesh B

RF Validation Automation

Version 0.1