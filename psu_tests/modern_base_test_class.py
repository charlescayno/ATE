import traceback
from copy import copy
from PySide2.QtCore import QObject, Signal, Slot
from psu_tests.definitions import TestStatus, MessageType
from psu_tests.ui_definitions import General_UI_Definitions, General_UI_Update_Definitions
from data_process.data_pipeline import TestTelemetryLogger
import psu_tests.test_object_imports as to_imports

class ModernBaseTestObject(QObject):
    """
    Thick base class for ATE tests.
    Encapsulates lifecycle management, equipment teardown, and telemetry reporting.
    """
    title = "Modern Base"
    short_title = "Modern_Base"
    i2c_test = False

    # Standard Signals (same as BaseTestObject)
    message = Signal(str, str, MessageType)
    progress = Signal(float)
    estimated_time = Signal(float)
    status_update = Signal(TestStatus)
    test_data_update = Signal(list)

    ui_definitions = General_UI_Definitions()
    ui_update = General_UI_Update_Definitions()

    def __init__(self, test_item):
        super().__init__()
        self.test_item = test_item
        self.parent = test_item.parent
        self.status = TestStatus.IN_QUEUE
        self.progress_pct = 0
        self.estimated_time_s = 0
        self.with_data = False
        self.logger = None

        self.unpack_test_item()

    def unpack_test_item(self):
        """Unpack test_conditions from the test_item. Subclasses can override if needed."""
        self.test_conditions = self.test_item.test_conditions

    def setup_equipment(self):
        """Bind equipment references. Assume parent.equipment is populated."""
        eq = self.parent.equipment
        self.ac_source = eq.ac_source
        self.electronic_load = eq.electronic_load_1
        self.power_meter = eq.power_meter
        self.usbpd_sink = eq.usbpd_sink

    def teardown_equipment(self):
        """Safe discharge sequence for all instruments."""
        try:
            if hasattr(self, 'electronic_load') and self.electronic_load:
                self.electronic_load.turn_off()
            if hasattr(self, 'ac_source') and self.ac_source:
                self.ac_source.turn_off()
            if hasattr(self, 'usbpd_sink') and self.usbpd_sink:
                self.usbpd_sink.usb_pd_initialize()
        except Exception as e:
            print(f"Error during teardown: {e}")

    def run(self):
        """
        The main thread execution wrapper.
        Handles the try/except/finally blocks and lifecycle signals.
        """
        try:
            self.status_update.emit(TestStatus.IN_PROGRESS)
            self.setup_equipment()
            self.setup_test()
            self.execute_sweep()

        except to_imports.TestStopped:
            print(f"Test {self.title} Stopped")
            self.status_update.emit(TestStatus.STOPPED)
        except to_imports.TestSkipped:
            print(f"Test {self.title} Skipped")
            self.status_update.emit(TestStatus.SKIPPED)
        except Exception as e:
            print(f"Test {self.title} Failed: {traceback.format_exc()}")
            self.status_update.emit(TestStatus.FAILED)
        else:
            self.status_update.emit(TestStatus.COMPLETE)
        finally:
            self.teardown_equipment()
            if self.logger:
                self.logger.close()

    def setup_test(self):
        """To be implemented by subclasses to initialize test-specific settings and logger headers."""
        raise NotImplementedError

    def execute_sweep(self):
        """To be implemented by subclasses to perform the actual instrument control and measurements."""
        raise NotImplementedError
    
    @classmethod
    def get_ui_definitions(cls, flags=None):
        return copy(cls.ui_definitions)

    @classmethod
    def get_ui_update_definitions(cls):
        return copy(cls.ui_update)

    def get_dict(self) -> dict:
        """To be implemented by subclass or parameters schema."""
        return {"NAME": self.title}
