import os
import pytest
from src import InstrumentController


def test_instrument_connect():
    ctrl = InstrumentController()
    assert not ctrl.connected
    ok = ctrl.connect('MOCK::1')
    assert ok
    assert ctrl.connected


def test_workflow_and_measurements(tmp_path):
    ctrl = InstrumentController()
    ctrl.connect('MOCK::1')
    assert ctrl.establish_call({'test': True}) is True
    screenshot = tmp_path / "shot.png"
    path = ctrl.capture_screenshot(str(screenshot))
    assert os.path.exists(path)
    measurements = ctrl.read_measurements()
    assert 'frequency_MHz' in measurements
    assert 'power_dBm' in measurements
