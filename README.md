# RF Automation

Basic RF automation to communicate with Device Under Test (DUT), CMW500, and a Spectrum Analyzer. This repository provides a Python starter project with a simple instrument controller stub, tests, and CI to help you begin development.

Features included:
- InstrumentController stub for connecting to instruments and performing basic operations
- Example usage script in src/
- Unit tests using pytest
- GitHub Actions CI to run tests on push and pull requests

Quickstart

1. Clone the repository:

   git clone https://github.com/RajeshB-RSE/RF-Automation-.git
   cd RF-Automation-

2. Create and activate a virtual environment (recommended):

   python -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   .\.venv\Scripts\activate  # Windows (PowerShell)

3. Install dependencies:

   pip install -r requirements.txt

4. Run the example script:

   python -m src.main

5. Run tests:

   pytest -q

Notes

- This repository currently contains a starter implementation (stubs) for instrument control. Replace the stubbed methods in src/instrument.py with real instrument communication code (e.g., using pyvisa or vendor SDKs) as you develop.
- If you want, tell me which instruments and drivers you will use (e.g., Rohde & Schwarz CMW500, Keysight, NI) and I can scaffold specific examples.
