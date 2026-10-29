from equipment.equipment import Equipment, visa_io
from equipment.power_meter_specs import *
from equipment.definitions import POWER_METER_LIST
from time import sleep, time

import pyvisa
import numpy as np

class IntegType:
    NORMAL = 0
    CONTINUOUS = 1

MAX_FAILED_POLLS = 2


class PowerMeterUnresponsive(Exception):
    """Raised by poll_basic_params when a meter should no longer be polled."""

class PowerMeter(Equipment):
    # Bench load PMs (WT310 / WT310E): instant P only on 2-port tests (timer forced 0 at setup).
    INTEGRATION_DISABLED_MODELS = frozenset({'WT310', 'WT310E'})

    def __init__(self, device, device_id, *, defer_hardware_init: bool = False):
        super().__init__(device, device_id)

        self.device_id = device_id
        self.device = device
        self.assumed_lazy_gpib = defer_hardware_init
        self.power_meter_object = None
        self.failed_polls = 0

        self.unpack_power_meter_specs()

        self._voltage = 0
        self._current = 0
        self._power = 0
        self._pf = 0
        self._thd = 0

        self._integration_mode = "NORMAL"
        self._integration_time = 0
        self._current_range = 0
        self._voltage_range = 0
        self._integration_status = None
        self._integration_done = False
        self._current_auto_range_status = False
        self._voltage_auto_range_status = False
        self._averaging_status = False

        last = self.device.resource_name.rfind("::")
        addr = self.device.resource_name[:last]
        self.description = f'{self.manufacturer} {self.model} {addr}'
        self.voltage_range_max = 0
        self.current_range_max = 0

        if not defer_hardware_init:
            self._initialize_hardware()
        else:
            print(
                f"[INFO] Power meter {self.description} registered (lazy GPIB — "
                "lock ignored at Detect; opens on first use)"
            )

    def _ensure_power_meter_object(self):
        if self.power_meter_object is not None:
            return
        model = self.model
        power_meter_model = POWER_METER_LIST[model]
        self.power_meter_object = power_meter_model(self.device, self.device_id)

    def _initialize_hardware(self):
        self._ensure_power_meter_object()
        self.set_preset()
        self.query_averaging_state()
        self.stop_integration()
        self.reset_integration()
        if not self.supports_fixed_range():
            self.auto_range_enable()

    def supports_fixed_range(self) -> bool:
        """Meters (WT500) whose range is left alone at connect and set only by the user."""
        return hasattr(POWER_METER_LIST.get(self.model), 'set_fixed_voltage_range')
        


    def set_preset(self):
        self._ensure_power_meter_object()
        self.power_meter_object.set_preset()  # TODO: Fix for WT3XX

    def update_basic_params(self):
        # Update later with better code
        # Updates all the parameters
        try:
            _ = self.voltage
            _ = self.current
            _ = self.power
            _ = self.pf
        except Exception as e:
            pass
        # _ = self.thd

    def is_poll_skipped(self) -> bool:
        """Lazy GPIB meters (locked at Detect) were never opened, so every read fails."""
        return self.assumed_lazy_gpib and self.power_meter_object is None

    def poll_basic_params(self, include_pf: bool = True):
        """Manual Control polling: bail out after the first failed read, and raise
        PowerMeterUnresponsive once the meter has failed MAX_FAILED_POLLS cycles in a row."""
        if self.is_poll_skipped():
            msg = f"{self.description}: lazy/locked GPIB meter, not polled"
            print(f"[POWER_METER] {msg}")
            raise PowerMeterUnresponsive(msg)
        # A dead meter costs ~1 s per read (timeout + retry), so stop at the first failure.
        if self.voltage is None:
            self.failed_polls += 1
            if self.failed_polls >= MAX_FAILED_POLLS:
                msg = f"{self.description}: no response for {self.failed_polls} polls, polling stopped"
                print(f"[POWER_METER] {msg}")
                raise PowerMeterUnresponsive(msg)
            return
        self.failed_polls = 0
        _ = self.current
        _ = self.power
        if include_pf:
            try:
                _ = self.pf
            except Exception as exc:
                print(
                    f"[POWER_METER] {self.description}: PF read skipped ({exc})"
                )
    
    def integration_disabled(self) -> bool:
        return (self.model or '').upper() in self.INTEGRATION_DISABLED_MODELS

    @visa_io
    def integrate(self, integration_time=60):
        if self.integration_disabled():
            return
        self.power_meter_object.integrate(integration_time)

    def integration_settings(self, mode:str, timer_s:int, reset=True):
        """ Sets the integration parameters of the Power Meter. 
        Resets the integration 

        Keyword Arguments:
        mode        --      Either NORMAL or Continuous
        timer       --      Tuple of (hhhh, mm, ss)
        """
        if self.integration_disabled():
            timer_s = 0
        try:
            self._stop_and_reset_integration()
            self.set_integration_mode(mode)
            self.set_integration_timer(timer_s)
            self.get_integration_timer()
        except Exception as e:
            raise e    
    
    @visa_io   
    def set_integration_mode(self, integ_mode:str = 'NORMAL'):
        """ Sets the integration parameters of the Power Meter. 
        
        Keyword Arguments:
        mode        --      Either NORMAL or Continuous
        """
        
        self.power_meter_object.set_integration_mode(integ_mode)
        self._integration_mode = integ_mode
        

    @visa_io
    def set_integration_timer(self, timer_s:int):
        """ Sets the integration timer of the power meter.

        Keyword Argument:
        timer_s     --      value of the timer in seconds
        """

        self.power_meter_object.set_integration_timer(timer_s)
        self._integration_time = timer_s
    
    @visa_io
    def get_integration_timer(self):
        """ Returns the integration timer value in seconds"""
        
        time_s = self.power_meter_object.get_integration_timer()
        return time_s

    def _stop_and_reset_integration(self) -> None:
        """WT500 error 813 if range/AUTO SCPI runs while integration is active."""
        try:
            self.stop_integration()
        except Exception:
            pass
        try:
            self.reset_integration()
        except Exception:
            pass

    def _integration_interval_s(self) -> float:
        """Configured integration window in seconds (0 = instantaneous power reads)."""
        try:
            timer_s = float(self.get_integration_timer())
        except (TypeError, ValueError):
            timer_s = 0.0
        if timer_s >= 1.0:
            return timer_s
        try:
            return float(getattr(self, '_integration_time', 0) or 0)
        except (TypeError, ValueError):
            return 0.0

    def start_integration(self):
        if self.integration_disabled():
            return
        interval_s = self._integration_interval_s()
        if interval_s >= 1.0:
            interval_txt = f" (interval {interval_s:g} s)"
        else:
            interval_txt = ""
        print(
            f"[POWER_METER] Power Meter {self.device_id}: Starting integration"
            f"{interval_txt}..."
        )
        try:
            if interval_s < 1.0:
                self.query_averaging_state()
                self.current_auto_range_query()
                self.voltage_auto_range_query()
            self._stop_and_reset_integration()
            self.power_meter_object.start_integration()
        except Exception as e:
            raise e
    
    @visa_io
    def stop_integration(self):
        self.power_meter_object.stop_integration()

    @visa_io
    def reset_integration(self):
        self.power_meter_object.reset_integration()
    
    @visa_io
    def poll_integration_status(self):
        interval_s = self._integration_interval_s()
        t0 = time()
        self.power_meter_object.poll_integration_status()
        self._integration_done = self.power_meter_object._integration_done
        self._integration_status = self.power_meter_object._integration_status
        elapsed_s = time() - t0
        status = self._integration_status
        if interval_s >= 1.0:
            print(
                f"[POWER_METER] Power Meter {self.device_id}: Integration stopped "
                f"after interval {interval_s:g} s "
                f"(elapsed {elapsed_s:.1f} s"
                f"{f', state {status}' if status else ''})"
            )
        else:
            print(
                f"[POWER_METER] Power Meter {self.device_id}: Integration stopped "
                f"(elapsed {elapsed_s:.1f} s"
                f"{f', state {status}' if status else ''})"
            )

    @visa_io
    def get_integrated_power(self, reset = True):
        """Returns the power equivalent of the total integrated energy"""
        power = self.power_meter_object.get_integrated_power(reset)
        self._stop_and_reset_integration()
        if self._integration_interval_s() < 1.0:
            self.voltage_auto_range_enable(self._voltage_auto_range_status)
            self.current_auto_range_enable(self._current_auto_range_status)
            self.enable_averaging(self._averaging_status)
        return power

    @property
    @visa_io
    def voltage(self):
        self._voltage = self.power_meter_object.voltage
        return self._voltage
        
    @property
    @visa_io
    def current(self):
        self._current = self.power_meter_object.current
        return self._current


    @property
    @visa_io
    def power(self):
        self._power = self.power_meter_object.power
        return self._power

    @visa_io
    def read_instant_power_w(self) -> float:
        """Active power read without starting a new integration cycle."""
        obj = self.power_meter_object
        if hasattr(obj, 'read_instant_power_w'):
            return float(obj.read_instant_power_w() or 0.0)
        self._power = obj.power
        return float(self._power or 0.0)

    @property
    @visa_io
    def pf(self):
        self._pf = self.power_meter_object.pf
        return self._pf

    @property
    @visa_io
    def thd(self):
        self._thd = self.power_meter_object.thd
        return self._thd
    
    @visa_io
    def get_current_range(self):
        self._current_range = self.power_meter_object.get_current_range()
        return self._current_range

    @visa_io
    def set_current_range(self, amps = None):
        self.power_meter_object.set_current_range(amps)
        self.get_current_range()
        
    @visa_io
    def set_current_range_max(self):
        self.power_meter_object.set_current_range_max()
        self.get_current_range()
        
    @visa_io
    def get_voltage_range(self):
        self._voltage_range = self.power_meter_object.get_voltage_range()
        return self._voltage_range

    @visa_io
    def set_voltage_range(self, volts = None):
        self.power_meter_object.set_voltage_range(volts)
        self.get_voltage_range()
    
    @visa_io
    def set_voltage_range_max(self):
        self.power_meter_object.set_current_range_max()
        self.get_voltage_range()

    @visa_io
    def set_fixed_voltage_range(self, volts):
        self.power_meter_object.set_fixed_voltage_range(volts)
        self._voltage_auto_range_status = False
        return self.power_meter_object.get_voltage_range()

    @visa_io
    def set_fixed_current_range(self, amps):
        self.power_meter_object.set_fixed_current_range(amps)
        self._current_auto_range_status = False
        return self.power_meter_object.get_current_range()

    def read_range_state(self):
        """Query only: (voltage_auto, voltage_range, current_auto, current_range), or None on failure."""
        obj = self.power_meter_object
        if obj is None:
            return None
        try:
            self._voltage_auto_range_status = obj.voltage_auto_range_query()
            self._voltage_range = obj.get_voltage_range()
            self._current_auto_range_status = obj.current_auto_range_query()
            self._current_range = obj.get_current_range()
        except Exception as e:
            print(f"[POWER_METER] {self.description}: range readback failed: {e}")
            return None
        return (
            self._voltage_auto_range_status,
            self._voltage_range,
            self._current_auto_range_status,
            self._current_range,
        )

    @visa_io
    def auto_range_enable(self, en:bool=True):
        self._stop_and_reset_integration()
        self.get_current_range()
        self.get_voltage_range()
        if en:
            self.set_current_range_max()
            self.set_voltage_range_max()
        else:
            self.set_current_range(self._current_range)
            self.set_voltage_range(self._voltage_range)
        self.power_meter_object.auto_range_enable(en)
        i_auto = bool(self.current_auto_range_query())
        v_auto = bool(self.voltage_auto_range_query())
        return i_auto and v_auto

    def ensure_auto_range_on(self, settle_s: float = 1.0) -> bool:
        """V/I auto-range ON only if currently off.

        Never forces RANGE MAX first: on WT310/WT310E that makes the meter hunt back
        down through its ranges and miss query timeouts.
        """
        obj = self.power_meter_object
        if obj is None:
            return False
        try:
            v_auto = bool(obj.voltage_auto_range_query())
            i_auto = bool(obj.current_auto_range_query())
        except Exception as exc:
            print(f"[POWER_METER] {self.description}: auto-range readback failed ({exc}); re-enabling")
            v_auto = i_auto = False
        if not (v_auto and i_auto):
            self._stop_and_reset_integration()
            try:
                if not v_auto:
                    obj.voltage_auto_range_enable(True)
                if not i_auto:
                    obj.current_auto_range_enable(True)
            except Exception as exc:
                print(f"[POWER_METER] {self.description}: auto-range enable failed: {exc}")
                return False
            if settle_s:
                sleep(settle_s)
            try:
                v_auto = bool(obj.voltage_auto_range_query())
                i_auto = bool(obj.current_auto_range_query())
            except Exception as exc:
                print(f"[POWER_METER] {self.description}: auto-range confirm failed: {exc}")
                return False
            print(f"[POWER_METER] {self.description}: auto-range V={v_auto} I={i_auto}")
        self._voltage_auto_range_status = v_auto
        self._current_auto_range_status = i_auto
        return v_auto and i_auto

    @visa_io
    def current_auto_range_enable(self, en:bool=True):
        self._stop_and_reset_integration()
        self.get_current_range()
        if not en:
            self.set_current_range(self._current_range)
        self.power_meter_object.current_auto_range_enable(en)
        # Non-None return stops visa_io from re-sending (each AUTO write sleeps 2 s).
        return bool(self.current_auto_range_query())
    
    @visa_io
    def current_auto_range_query(self):
        self._current_auto_range_status = self.power_meter_object.current_auto_range_query()
        return self._current_auto_range_status
    
    @visa_io
    def current_auto_range_toggle(self):
        self.power_meter_object.current_auto_range_toggle()
        self.current_auto_range_query()

    @visa_io
    def voltage_auto_range_enable(self, en:bool=True):
        self._stop_and_reset_integration()
        self.get_voltage_range()
        if not en:
            self.set_voltage_range(self._voltage_range)
        self.power_meter_object.voltage_auto_range_enable(en)
        return bool(self.voltage_auto_range_query())

    @visa_io
    def voltage_auto_range_query(self):
        self._voltage_auto_range_status = self.power_meter_object.voltage_auto_range_query()
        return self._voltage_auto_range_status  

    @visa_io
    def voltage_auto_range_toggle(self):
        self.power_meter_object.voltage_auto_range_toggle()
        self.voltage_auto_range_query()

    @visa_io
    def auto_range_query(self):
        v_auto = self.power_meter_object.voltage_auto_range_query()
        i_auto = self.power_meter_object.current_auto_range_query()
        auto_range_status = v_auto and i_auto

        return auto_range_status
    
    @visa_io
    def auto_range_toggle(self):
        self.current_auto_range_query()
        self.voltage_auto_range_query()

        self.voltage_auto_range_enable(not self._voltage_auto_range_status)
        self.current_auto_range_enable(not self._current_auto_range_status)

    @visa_io
    def enable_averaging(self, en:bool=True):
        self.power_meter_object.enable_averaging(en)
        self.query_averaging_state()
    
    @visa_io
    def query_averaging_state(self):
        self._averaging_status = self.power_meter_object.query_averaging_state()
        return self._averaging_status

    @visa_io
    def averaging_toggle(self):
        self.power_meter_object.averaging_toggle()
        self.query_averaging_state()

    def get_harmonics(self):
        harmonic_content, percent_content = self.power_meter_object.get_harmonics()
        return harmonic_content, percent_content

    @visa_io
    def reset(self):
        self.power_meter_object.reset()
    
    def unpack_power_meter_specs(self):
        model = self.model
        if model not in POWER_METER_LIST:
            raise KeyError(f"Unknown power meter model {model!r}")
        if not self.assumed_lazy_gpib:
            self._ensure_power_meter_object()

    def cleanup(self):
        self.close()
        
    
