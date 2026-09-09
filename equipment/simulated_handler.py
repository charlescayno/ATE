"""
equipment/simulated_handler.py
Virtual instrument simulation Hardware Abstraction Layer (HAL) for PI ATE.
Enables offline development, test automation, and CI/CD pipelines without physical instruments.
"""
import os
import math
import random
import numpy as np
from PIL import Image, ImageDraw

from equipment.definitions import EquipmentType
from equipment.ac_source import AC_SOURCE_COUPLING
from equipment.handler import EquipmentHandler

class VirtualCircuitState:
    """Shared physical state of the simulated Unit Under Test (UUT) and bench instruments."""
    def __init__(self):
        self.vin = 115.0
        self.freq = 60.0
        self.ac_on = False
        self.nominal_eff = 0.90  # 90% nominal efficiency
        self.pf = 0.96
        # Multi-channel load state: channel_idx -> {target_vout, iout, load_on}
        self.loads = {
            1: {'target_vout': 5.0, 'iout': 0.0, 'load_on': False},
            2: {'target_vout': 12.0, 'iout': 0.0, 'load_on': False},
            3: {'target_vout': 12.0, 'iout': 0.0, 'load_on': False},
            4: {'target_vout': 12.0, 'iout': 0.0, 'load_on': False},
            5: {'target_vout': 12.0, 'iout': 0.0, 'load_on': False},
            6: {'target_vout': 12.0, 'iout': 0.0, 'load_on': False},
        }

    @property
    def target_vout(self):
        return self.loads[1]['target_vout']
    @target_vout.setter
    def target_vout(self, val):
        self.loads[1]['target_vout'] = float(val)

    @property
    def iout(self):
        return self.loads[1]['iout']
    @iout.setter
    def iout(self, val):
        self.loads[1]['iout'] = float(val)

    @property
    def load_on(self):
        return any(ld['load_on'] for ld in self.loads.values())
    @load_on.setter
    def load_on(self, val):
        self.loads[1]['load_on'] = bool(val)

    def get_total_pout(self):
        """Sum the active power across all loaded channels."""
        total = 0.0
        for ch, ld in self.loads.items():
            if ld['load_on']:
                droop = ld['iout'] * 0.02
                v_act = max(0.0, ld['target_vout'] - droop)
                total += v_act * ld['iout']
        return total


class SimulatedACSource:
    def __init__(self, state: VirtualCircuitState):
        self.state = state
        self.model = '61501'
        self.manufacturer = 'Chroma'
        self.serial = 'SIM-AC-001'
        self.description = f'{self.manufacturer} {self.model} {self.serial} (Simulated)'
        self.device_id = f'{self.manufacturer},{self.model},{self.serial},1.0.0'
        self.details = self.device_id
        self.address = 'GPIB0::1::INSTR'
        self.coupling = 'AC'
        self.offset = 0.0
        self.ac_slew_rate = 9.9e37
        self.dc_slew_rate = 9.9e37
        self.freq_slew_rate = 9.9e37

    @property
    def voltage(self):
        return self.state.vin if self.state.ac_on else 0.0

    @voltage.setter
    def voltage(self, val):
        self.state.vin = float(val)

    @property
    def frequency(self):
        return self.state.freq

    @frequency.setter
    def frequency(self, val):
        self.state.freq = float(val)

    def turn_on(self):
        self.state.ac_on = True

    def turn_off(self):
        self.state.ac_on = False

    def set_voltage(self, voltage: float):
        self.state.vin = float(voltage)

    def set_voltage_with_coupling(self, voltage: float, coupling='AC'):
        self.state.vin = float(voltage)
        self.coupling = str(coupling)

    def set_frequency(self, freq: float):
        self.state.freq = float(freq)

    def set_freq(self, freq: float):
        self.set_frequency(freq)

    def update_status(self): pass
    def cleanup(self): self.turn_off()
    def close(self): pass
    def write(self, cmd): pass


class ChannelIntDict(int):
    """
    Polymorphic channel wrapper: behaves as integer channel index (1),
    supports len() and dictionary-style indexing self.channel[ch] to maintain
    full compatibility with both mainframe and modular electronic load callers.
    """
    def __new__(cls, val, module):
        return super().__new__(cls, val)

    def __init__(self, val, module):
        self.module = module

    def __len__(self):
        return 1

    def __getitem__(self, item):
        return self.module


class SimulatedElectronicLoadModule:
    def __init__(self, state: VirtualCircuitState, channel_idx: int = 1):
        self.state = state
        self.channel_idx = channel_idx
        self.model = '63102A'
        self.manufacturer = 'Chroma'
        self.mainframe_model = '6314A'
        self.serial = f'SIM-LOAD-00{channel_idx}'
        self.channel = ChannelIntDict(channel_idx, self)
        self.channel_id = [self.manufacturer, self.model, self.serial, '1.00']
        self.description = f'{self.manufacturer} {self.mainframe_model} {self.model} Ch{channel_idx} (Simulated)'
        self.device_id = f'{self.manufacturer},{self.model},{self.serial},1.0.0'
        self.details = self.description
        self.address = f'GPIB0::{2 + channel_idx}::INSTR'
        self._active_level = '1'
        self.active_channel_status = 1
        self.active_channel_short = 0
        self.crh_max_r = 50000.0

    @property
    def _ch(self):
        if self.channel_idx not in self.state.loads:
            self.state.loads[self.channel_idx] = {'target_vout': 12.0, 'iout': 0.0, 'load_on': False}
        return self.state.loads[self.channel_idx]

    @property
    def voltage(self):
        if not self.state.ac_on:
            return 0.0
        droop = self._ch['iout'] * 0.02
        return max(0.0, self._ch['target_vout'] - droop)

    @property
    def current(self):
        return self._ch['iout'] if (self._ch['load_on'] and self.state.ac_on) else 0.0

    @property
    def cc(self):
        return self._ch['iout']

    @cc.setter
    def cc(self, val):
        self._ch['iout'] = float(val)

    @property
    def cv(self): return self._ch['target_vout']
    @cv.setter
    def cv(self, val): self._ch['target_vout'] = float(val)

    @property
    def cr(self): return 100.0
    @cr.setter
    def cr(self, val): pass

    @property
    def cp(self): return self.voltage * self.current
    @cp.setter
    def cp(self, val): pass

    def turn_on(self):
        self._ch['load_on'] = True

    def turn_off(self):
        self._ch['load_on'] = False

    def turn_on_all(self):
        for ld in self.state.loads.values():
            ld['load_on'] = True

    def turn_off_all(self):
        for ld in self.state.loads.values():
            ld['load_on'] = False

    def set_load(self, vout: float, iout: float, eload_type=None):
        self._ch['target_vout'] = float(vout)
        self._ch['iout'] = float(iout)

    def set_current(self, iout: float):
        self._ch['iout'] = float(iout)

    def set_active_level(self, level): pass
    def set_cc_static_slew(self, slew): pass
    def short_on(self): pass
    def short_off(self): pass
    def reset_values(self): pass
    def cleanup(self): self.turn_off()
    def close(self): pass
    def write(self, cmd): pass


class SimulatedPowerMeter:
    def __init__(self, state: VirtualCircuitState, is_source: bool = True, channel_idx: int = 1):
        self.state = state
        self.is_source = is_source
        self.channel_idx = channel_idx
        self.model = 'WT310'
        self.manufacturer = 'Yokogawa'
        self.serial = 'SIM-PM-001' if is_source else f'SIM-PM-00{1 + channel_idx}'
        role_label = 'Source' if is_source else f'Load {channel_idx}'
        self.description = f'{self.manufacturer} {self.model} {role_label} (Simulated)'
        self.device_id = f'{self.manufacturer},{self.model},{self.serial},1.0.0'
        self.details = self.description
        self.address = f'GPIB0::{3 if is_source else (10 + channel_idx)}::INSTR'
        self._current_auto_range_status = True
        self._voltage_auto_range_status = True
        self._averaging_status = False

    @property
    def _ch(self):
        if self.channel_idx not in self.state.loads:
            self.state.loads[self.channel_idx] = {'target_vout': 12.0, 'iout': 0.0, 'load_on': False}
        return self.state.loads[self.channel_idx]

    @property
    def voltage(self):
        if self.is_source:
            return self.state.vin if self.state.ac_on else 0.0
        if not self.state.ac_on:
            return 0.0
        droop = self._ch['iout'] * 0.02
        noise = random.gauss(0, 0.003)
        return max(0.0, round(self._ch['target_vout'] - droop + noise, 3))

    @property
    def current(self):
        if self.is_source:
            if not self.state.ac_on:
                return 0.0
            p_in = self.power
            v_in = max(self.voltage, 1.0)
            return round(p_in / (v_in * self.pf), 4)
        return round(self._ch['iout'], 4) if (self._ch['load_on'] and self.state.ac_on) else 0.0

    @property
    def power(self):
        if self.is_source:
            if not self.state.ac_on:
                return 0.0
            p_out = self.state.get_total_pout()
            if p_out <= 0:
                p_out = 0.12  # Standby power
            return round(p_out / self.state.nominal_eff, 3)
        v = self.voltage
        i = self.current
        return round(v * i, 3)

    @property
    def pf(self):
        return self.state.pf if self.state.ac_on else 0.0

    @property
    def power_factor(self):
        return self.pf

    @property
    def thd(self):
        return 4.8 if self.state.ac_on else 0.0

    # Backwards-compatibility internal cache properties
    @property
    def _voltage(self): return self.voltage
    @property
    def _current(self): return self.current
    @property
    def _power(self): return self.power
    @property
    def _pf(self): return self.pf
    @property
    def _thd(self): return self.thd

    def auto_range_enable(self, en: bool = True): pass
    def current_auto_range_enable(self, en: bool = True): pass
    def voltage_auto_range_enable(self, en: bool = True): pass
    def set_current_range(self, *args, **kwargs): pass
    def get_current_range(self): return 5.0
    def set_current_range_max(self): pass
    def set_voltage_range_max(self): pass
    def integration_settings(self, mode="NORMAL", timer_s=0): pass
    def start_integration(self): pass
    def stop_integration(self): pass
    def reset_integration(self): pass
    def get_integration_timer(self): return "0:00:00"
    def set_integration_timer(self, timer_s: int): pass
    def poll_integration_status(self): return "STOP"
    def get_integrated_power(self, reset=True): return self.power
    def get_integrated_energy(self): return 0.0
    def query_averaging_state(self): return True
    def current_auto_range_query(self): return True
    def voltage_auto_range_query(self): return True
    def get_harmonics(self): return {}, {}
    def close(self): pass
    def write(self, cmd): pass


class DummyScopeChannel:
    def __init__(self, ch_num):
        self.channel = ch_num
        self.scale = 50.0
        self.position = 0.0
        self.offset = 0.0


class SimulatedOscilloscope:
    def __init__(self, state: VirtualCircuitState):
        self.state = state
        self.model = 'RTM3004'
        self.manufacturer = 'Rohde&Schwarz'
        self.serial = 'SIM-DSO-001'
        self.description = f'{self.manufacturer} {self.model} (Simulated)'
        self.device_id = f'{self.manufacturer},{self.model},{self.serial},1.0.0'
        self.details = self.device_id
        self.address = 'TCPIP::192.168.1.100::INSTR'
        self.channel = {i: DummyScopeChannel(i) for i in range(1, 5)}
        self._trigger_mode = 'AUTO'
        self._time_scale = 1e-6
        self._time_position = 0.0
        self.record_length = 10000

    def trigger_mode(self, mode='AUTO'):
        self._trigger_mode = mode
        return self._trigger_mode

    def trigger_status(self):
        return 0  # Trigger locked/completed

    def time_scale(self, scale=None):
        if scale is not None:
            self._time_scale = scale
        return self._time_scale

    def time_position(self, pos=None):
        if pos is not None:
            self._time_position = pos
        return self._time_position

    def channel_settings(self, channel, scale=None, position=None, coupling=None, bandwidth=None, invert=None):
        pass

    def edge_trigger(self, channel=1, level=0.0, slope='POS'):
        pass

    def display_channel(self, channel: int, enable: bool): pass
    def scale_channel(self, channel: int, scale: float): pass
    def position_channel(self, channel: int, pos: float): pass
    def set_time_scale(self, scale: float): self._time_scale = scale
    def set_trigger_channel(self, channel: int): pass
    def set_trigger_level(self, level: float): pass

    def add_zoom(self, *args, **kwargs): pass
    def remove_zoom(self, *args, **kwargs): pass
    def measure(self, *args, **kwargs): pass
    def setup_ripple(self, *args, **kwargs): pass

    def run(self): pass
    def run_single(self): pass
    def stop(self): pass

    def get_measure(self, channel: int, meas_type: str = 'MAX'):
        if channel == 1:
            peak = (self.state.vin * 1.414) + 115.0 + random.gauss(0, 1.5)
            return (['Max'], [round(peak, 2)])
        elif channel == 2:
            peak = self.state.iout * 1.4 + 0.15 + random.gauss(0, 0.02)
            return (['Max'], [round(peak, 3)])
        return (['Max'], [5.0])

    def get_measure_all(self):
        return [
            {'channel': 1, 'labels': ['Max'], 'values': [round((self.state.vin * 1.414) + 115.0, 2)]},
            {'channel': 2, 'labels': ['Max'], 'values': [round(self.state.iout * 1.4 + 0.15, 3)]}
        ]

    def get_screenshot(self, filename='default.png', path='.'):
        """Generates a realistic oscilloscope graticule display."""
        img = Image.new('RGB', (800, 480), color=(12, 18, 24))
        draw = ImageDraw.Draw(img)

        # Draw grid
        for x in range(0, 800, 80):
            draw.line([(x, 0), (x, 480)], fill=(32, 44, 56), width=1)
        for y in range(0, 480, 48):
            draw.line([(0, y), (800, y)], fill=(32, 44, 56), width=1)

        # Generate synthetic ringing waveform
        t = np.linspace(0, 10, 800)
        v_peak_px = 140
        decay = np.exp(-0.4 * (t % 2.5))
        oscillation = np.cos(2 * np.pi * 3.5 * t)
        y_drain = 240 - v_peak_px * decay * oscillation
        pts_drain = list(zip(range(800), y_drain.astype(int)))
        draw.line(pts_drain, fill=(255, 215, 0), width=2)

        # Current waveform
        y_curr = 360 - 50 * (1 - np.exp(-0.8 * (t % 2.5)))
        pts_curr = list(zip(range(800), y_curr.astype(int)))
        draw.line(pts_curr, fill=(0, 255, 200), width=2)

        # Draw on-screen telemetry
        draw.text((20, 15), 'R&S RTM3004 [SIMULATED VIRTUAL SCOPE]', fill=(220, 220, 220))
        draw.text((20, 35), f'CH1 (Vds): 50V/div  Peak={round((self.state.vin*1.414)+115.0, 1)}V', fill=(255, 215, 0))
        draw.text((20, 55), f'CH2 (Ids): 1A/div   Peak={round(self.state.iout*1.4+0.15, 2)}A', fill=(0, 255, 200))
        draw.text((620, 15), f'Vin: {self.state.vin}VAC', fill=(180, 180, 180))
        draw.text((620, 35), f'Iout: {self.state.iout}A', fill=(180, 180, 180))
        draw.text((620, 55), 'Trig: AUTO (Locked)', fill=(50, 255, 50))

        full_path = os.path.join(path, filename)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        img.save(full_path)
        return full_path

    def close(self): pass
    def write(self, cmd): pass


class SimulatedSinkController:
    """Simulates USB-PD Sink (PISinkController / STM32SinkController)."""
    def __init__(self):
        self.serial_number = 'SIM-SINK-001'
        self.description = 'Virtual USB-PD Sink Controller (Simulated)'
        self.device_id = 'PISinkController,SIM-001,1.0'
        self.details = self.description
        self.source_cap_count = 4
        self.source_capabilities = [
            {'pdo_index': 1, 'type': 'FIXED', 'voltage': 5.0, 'max_current': 3.0},
            {'pdo_index': 2, 'type': 'FIXED', 'voltage': 9.0, 'max_current': 3.0},
            {'pdo_index': 3, 'type': 'FIXED', 'voltage': 15.0, 'max_current': 3.0},
            {'pdo_index': 4, 'type': 'FIXED', 'voltage': 20.0, 'max_current': 3.25},
        ]

    def usb_pd_initialize(self): return True
    def get_status(self, serial_number=None): return True
    def get_source_capabilities(self): return self.source_capabilities
    def request_pdo(self, pdo_index, current_A=None): return True
    def request_pps(self, voltage_V, current_A): return True
    def pps_thread_cleanup(self): pass
    def cleanup(self): pass
    def close(self): pass


class SimulatedEquipmentHandler(EquipmentHandler):
    """
    Complete drop-in simulated EquipmentHandler subclass.
    Provides identical attribute signatures, roles, and device lists without VISA.
    """
    def __init__(self, parent):
        self.parent = parent
        self.state = VirtualCircuitState()

        # Virtual instruments
        self.ac_source = SimulatedACSource(self.state)
        self.dc_source = None
        self.electronic_load_1 = SimulatedElectronicLoadModule(self.state, channel_idx=1)
        self.electronic_load_2 = SimulatedElectronicLoadModule(self.state, channel_idx=2)
        self.electronic_load_3 = SimulatedElectronicLoadModule(self.state, channel_idx=3)
        self.electronic_load_4 = SimulatedElectronicLoadModule(self.state, channel_idx=4)
        self.electronic_load_5 = None
        self.electronic_load_6 = None

        self.power_meter_source = SimulatedPowerMeter(self.state, is_source=True)
        self.power_meter_load_1 = SimulatedPowerMeter(self.state, is_source=False, channel_idx=1)
        self.power_meter_load_2 = SimulatedPowerMeter(self.state, is_source=False, channel_idx=2)
        self.power_meter_load_3 = SimulatedPowerMeter(self.state, is_source=False, channel_idx=3)
        self.power_meter_load_4 = SimulatedPowerMeter(self.state, is_source=False, channel_idx=4)
        self.power_meter_load_5 = None
        self.power_meter_load_6 = None

        self.oscilloscope = SimulatedOscilloscope(self.state)
        self.usbpd_sink = SimulatedSinkController()
        self.i2c_controller = None

        # Equipment lists
        self.ac_sources = [self.ac_source]
        self.dc_sources = []
        self.e_loads = [
            self.electronic_load_1,
            self.electronic_load_2,
            self.electronic_load_3,
            self.electronic_load_4
        ]
        self.e_load_mainframes = []
        self.power_meters = [
            self.power_meter_source,
            self.power_meter_load_1,
            self.power_meter_load_2,
            self.power_meter_load_3,
            self.power_meter_load_4
        ]
        self.oscilloscopes = [self.oscilloscope]
        self.sink_controllers = [self.usbpd_sink]
        self.i2c_controllers = []
        self.gpib_resource = []

        # Role mappings
        self.power_meter_roles = [
            self.power_meter_source,
            self.power_meter_load_1,
            self.power_meter_load_2,
            self.power_meter_load_3,
            self.power_meter_load_4,
            None
        ]
        self.electronic_load_roles = [
            self.electronic_load_1,
            self.electronic_load_2,
            self.electronic_load_3,
            self.electronic_load_4,
            None,
            None
        ]
        self.sink_controller_1 = self.usbpd_sink
        self.sink_controller_2 = None
        self.sink_controller_3 = None
        self.sink_controller_4 = None
        self.sink_controller_roles = [self.sink_controller_1, None, None, None]

        self.i2c_controller_1 = None
        self.i2c_controller_2 = None
        self.i2c_controller_3 = None
        self.i2c_controller_4 = None
        self.i2c_controller_roles = [None, None, None, None]

    def update_accessible_equipment(self): pass
    def update_accessible_visa_equipment(self): pass
    def clear_accessible_visa_equipment(self): pass
    def update_accessible_sink_controllers(self):
        return self.sink_controllers, self.i2c_controllers
    def check_scope_availability(self, address='', get_default=False):
        return True
    def apply_saved_equipment_roles(self, config):
        return True
    def auto_set_equipment_roles(self): pass
    def auto_set_ac_source_roles(self): pass
    def auto_set_dc_source_roles(self): pass
    def auto_set_electronic_load_roles(self): pass
    def auto_set_power_meter_roles(self): pass
    def auto_set_sink_controller_roles(self):
        self.sink_controller_1 = self.usbpd_sink
        self.usbpd_sink = self.sink_controller_1
        self.sink_controller_roles = [self.sink_controller_1, None, None, None]

    def auto_set_i2c_controller_roles(self):
        self.i2c_controller_roles = [None, None, None, None]

    def reset_sink_controller_roles(self):
        self.sink_controller_1 = self.usbpd_sink
        self.sink_controller_2 = None
        self.sink_controller_3 = None
        self.sink_controller_4 = None

    def reset_i2c_controller_roles(self):
        self.i2c_controller_1 = None
        self.i2c_controller_2 = None
        self.i2c_controller_3 = None
        self.i2c_controller_4 = None

    def reset_power_meter_roles(self):
        self.power_meter_source = self.power_meters[0] if len(self.power_meters) > 0 else None
        self.power_meter_load_1 = self.power_meters[1] if len(self.power_meters) > 1 else None
        self.power_meter_load_2 = self.power_meters[2] if len(self.power_meters) > 2 else None
        self.power_meter_load_3 = self.power_meters[3] if len(self.power_meters) > 3 else None
        self.power_meter_load_4 = self.power_meters[4] if len(self.power_meters) > 4 else None

    def reset_electronic_load_roles(self):
        self.electronic_load_1 = self.e_loads[0] if len(self.e_loads) > 0 else None
        self.electronic_load_2 = self.e_loads[1] if len(self.e_loads) > 1 else None
        self.electronic_load_3 = self.e_loads[2] if len(self.e_loads) > 2 else None
        self.electronic_load_4 = self.e_loads[3] if len(self.e_loads) > 3 else None

    def input_supply_eload_discharge_sequence(self, iout_A, coupling=AC_SOURCE_COUPLING.AC):
        self.electronic_load_1.cc = iout_A
        self.electronic_load_1.turn_on()
        self.ac_source.turn_off()
        self.electronic_load_1.turn_off()
        if self.electronic_load_2:
            self.electronic_load_2.turn_off()