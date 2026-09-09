# Threading Architecture in Power Integrations ATE (PI ATE)

This document provides a detailed breakdown of how threading, asynchronous orchestration, and inter-thread communication are implemented across the **PI ATE** platform.

---

## 1. Concurrency Model Overview

Automated Test Equipment (ATE) applications present a classic concurrency challenge:
- **Long-Running Blocking Operations**: Bench instruments (AC power sources, electronic loads, power analyzers, oscilloscopes) communicate over serial, GPIB, USB-TMC, or Ethernet protocols. Operations such as line soaking, voltage ramping, scope trigger hunting, and USB-PD capability negotiation often take anywhere from several seconds to tens of minutes.
- **UI Responsiveness**: If these blocking I/O calls were executed on the main GUI thread, the user interface would freeze immediately, Windows would flag the window as *"Not Responding"*, and the operator would lose the ability to abort or view real-time telemetry.

To solve this, PI ATE strictly decouples the **Main UI Thread** from all **Instrument I/O & Execution Threads**.

```
+-----------------------------------------------------------------------------------------+
|                                    MAIN GUI THREAD                                      |
|                                                                                         |
|  +--------------------+      200ms Tick       +--------------------------------------+  |
|  |    PySide2 UI      | <-------------------> | QTimer (test_plan_update_service)    |  |
|  |  (Window / Tables) |                       | - Dispatches next queued test item   |  |
|  +--------------------+                       | - Updates countdowns & progress bars |  |
|           ^                                   +--------------------------------------+  |
|           |                                                      |                      |
|           | Slots:                                               | Spawns               |
|           | - popup_message()                                    v                      |
|           | - update_test_data()                      +----------------------+          |
|           | - update_progress()                       |  QThread (Container) |          |
|           | - update_object_status()                  +----------------------+          |
|           |                                                      |                      |
+-----------|------------------------------------------------------|----------------------+
            | Signals (Qt.QueuedConnection)                        | worker.moveToThread()
+-----------|------------------------------------------------------|----------------------+
|           |                                                      v                      |
|  +-----------------------------------------------------------------------------------+  |
|  |                         BACKGROUND WORKER THREAD (QThread)                        |  |
|  |                                                                                   |  |
|  |   Test Worker (QObject / BaseTestObject)                                          |  |
|  |   - worker.run() -> test_loop()                                                   |  |
|  |   - VISA SCPI Queries (GPIB / TCPIP / USB-TMC)                                    |  |
|  |   - Instrument Delays & Soaking (time.sleep)                                      |  |
|  |   - Excel Workbook Generation & Image Embedding                                   |  |
|  |   - Checks test_control_flags['StopTest'] cooperatively                           |  |
|  +-----------------------------------------------------------------------------------+  |
|                                                                                         |
+-----------------------------------------------------------------------------------------+
```

---

## 2. Core Pattern: Qt Worker Object Pattern (`moveToThread`)

In modern Qt programming (PySide2 / PyQt5), subclassing `QThread` and overriding `run()` is considered an anti-pattern for complex state machines because the `QThread` object itself still lives in the thread that created it. 

PI ATE follows the canonical **Worker Object Pattern**:
1. The worker class inherits from `QObject` (via `BaseTestObject`).
2. An independent `QThread` instance is created.
3. The worker is pushed to that thread using `worker.moveToThread(thread)`.
4. The thread's `started` signal is linked to the worker's `run()` method.

### Implementation in `psu_tests/tests.py`

When an individual `TestItem` is triggered by the test plan, it prepares the thread and establishes the signal/slot bridges:

```python
class TestItem():
    ...
    def run(self):
        """ Run the test object of the TestItem Object """
        self.status = TestStatus.IN_PROGRESS
        self.worker: TemplateTest = self.test_object

        # 1. Move the worker QObject to the separate QThread
        self.worker.moveToThread(self.test_routine_thread)

        # 2. Wire thread lifecycle signals
        self.test_routine_thread.started.connect(self.worker.run)
        self.test_routine_thread.finished.connect(self.update_status)
        
        # 3. Connect worker telemetry signals to TestItem slots on the Main Thread
        self.worker.status_update.connect(self.update_object_status)
        self.worker.estimated_time.connect(self.update_estimated_time)
        self.worker.progress.connect(self.update_progress)
        self.worker.message.connect(self.popup_message)
        
        try:
            self.worker.test_data_update.connect(self.update_test_data)
        except Exception:
            print("Add test data update for this test")

        # 4. Start the OS thread; this triggers worker.run() inside the new thread context
        self.test_routine_thread.start()
```

### Preventing Python Garbage Collection of Running Threads

In Python, local variables that fall out of scope are eligible for immediate garbage collection. If a `QThread` instance is garbage collected while its OS thread is still executing, the application crashes with a segmentation fault (`QThread: Destroyed while thread is still running`).

To prevent this, `page_controls/add_test.py` explicitly binds the active thread reference to both the `AddTestPageHandler` instance and the top-level `MainWindow` (`self.parent`):

```python
# From page_controls/add_test.py:
self.test_routine_thread = QThread()
self.test_routine_thread.finished.connect(self.test_routine_thread_cleanup)
test_item.test_routine_thread = self.test_routine_thread

# Bind thread to parent to prevent garbage collection from deleting it
self.parent.test_routine_thread = self.test_routine_thread
```

---

## 3. The Orchestration Engine: Main Thread `QTimer`

Rather than blocking the main thread while waiting for a worker to finish, PI ATE uses a **polling state machine** powered by `QTimer`.

### Timer Initialization (`page_controls/add_test.py`)

```python
def setup_testplan_update_timer(self):
    """Setup the timer that will run the update loop for both UI and TestPlan."""
    self.test_plan_update_timer = QTimer(self.parent)
    self.test_plan_update_timer.timeout.connect(self.test_plan_update_service)
```

When the user clicks the **Run** button, `run_tests()` starts this timer with an interval of `TEST_PLAN_UPDATE_TIMER = 200` ms:

```python
def run_tests(self):
    self.ui.btn_add_tests_run.setEnabled(False)
    ...
    self.output_folder_path = self.get_output_folder_path()
    self.test_plan.output_folder_path = self.output_folder_path
    self.test_plan.status = TestStatus.IN_QUEUE

    # Start the 200ms periodic update loop
    self.test_plan_update_timer.start(TEST_PLAN_UPDATE_TIMER)
    self.select_current_run_results_folder()
```

### The Update Service Loop (`test_plan_update_service`)

Every 200 milliseconds, the timer fires on the main thread to manage the queue:

```python
def test_plan_update_service(self):
    global test_control_flags
    test_plan = self.test_plan
    test_plan.update_status()

    # Case A: User clicked Stop
    if test_plan.status == TestStatus.STOPPED:
        self.test_plan_update_timer.stop()

    # Case B: Test plan is ready for the next test
    elif test_plan.status == TestStatus.IN_QUEUE:
        for test_item_index, test_item in enumerate(test_plan.test_items):
            if test_item.status == TestStatus.IN_QUEUE:
                # Reset cooperative abort flags
                test_control_flags['StopTest'] = False
                test_control_flags['SkipTest'] = False

                # Allocate fresh QThread for this test item
                self.test_routine_thread = QThread()
                self.test_routine_thread.finished.connect(self.test_routine_thread_cleanup)
                test_item.test_routine_thread = self.test_routine_thread
                self.parent.test_routine_thread = self.test_routine_thread 

                # Recreate test object to ensure fresh worker state
                test_item.generate_test_object()
                test_object = test_item.test_object
                test_object.output_folder_path = self.output_folder_path
                
                # Launch worker thread
                test_item.run()
                self.ui.table_add_tests_test_list.setCurrentIndex(
                    self.ui.table_add_tests_test_list.model().index(test_item_index, 0)
                )
                break  

    # Case C: All tests have concluded
    elif test_plan.status == TestStatus.COMPLETE:
        self.test_routine_thread = None
        self.parent.test_routine_thread = None
        self.test_plan_update_timer.stop()
        self.update_test_list_control_buttons_state()
        ...
        self.parent.msg_box_info('Test Info', 'Test Complete', MessageType.INFO)

    # Decrement live visual countdowns for active test
    for test_item in test_plan.test_items:
        if test_item.test_object.status == TestStatus.IN_PROGRESS:
            if test_item.test_object.estimated_time_s >= 0.2:
                test_item.test_object.estimated_time_s -= 0.2
            else:
                test_item.test_object.estimated_time_s = 0

    # Refresh the UI table view
    self.update_test_list_details()
    self.update_test_list_control_buttons_state()
```

---

## 4. Inter-Thread Communication via Signals & Slots

Qt enforces a strict rule: **GUI widgets (`QWidget`, `QLabel`, `QTableWidget`, etc.) can ONLY be accessed and modified from the Main GUI Thread**. Direct manipulation of widgets from a background thread results in memory corruption, rendering artifacts, or immediate hard crashes.

PI ATE passes all measurement telemetry, status notifications, and user alerts across thread boundaries strictly via **Qt Signals and Slots**. Because the sender (`worker` in `QThread`) and receiver (`TestItem` / `MainWindow` in Main Thread) have different thread affinities, Qt automatically uses `Qt.QueuedConnection`.

### Base Signal Definitions (`psu_tests/base_test_class.py`)

All test routines inherit from `BaseTestObject`:

```python
class BaseTestObject(QObject):
    title = "Base"
    i2c_test = False

    # Inter-thread communication signals
    message = Signal(str, str, MessageType)     # (Title, Message Body, Message Type)
    progress = Signal(float)                    # Percentage complete (0.0 to 100.0)
    estimated_time = Signal(float)              # Time remaining in seconds
    status_update = Signal(TestStatus)          # Lifecycle enum (IN_PROGRESS, COMPLETE, etc.)
    test_data_update = Signal(list)             # [plottables_list, DataTable]
```

### Telemetry Pipeline Example

During a test sweep (e.g., in `EfficiencyTest` or `SteadyStateWaveformCaptureTest`), the worker queries instruments and emits telemetry:

```python
# Inside worker thread (test_loop):
data_point = [vin_meas, freq_meas, pin_meas, pf_meas, vout_meas, iout_meas, pout_meas, eff_pct]
self.test_data_table.append_data(data_point)

# Emit data across thread boundary to update graphs & table without blocking
self.test_data_update.emit([self.plottables, self.test_data_table])

# Emit progress and status
self.progress.emit((current_step / total_steps) * 100.0)
```

On the main thread, `TestItem.update_test_data()` receives the payload:

```python
# In psu_tests/tests.py (Main Thread context):
@Slot(list)
def update_test_data(self, test_data):
    """ Slot to receive the test data sent by the test object thread """
    self.with_test_data = True
    self.plottables = test_data[0]
    self.test_data_table = test_data[1]
```

---

## 5. Synchronous Modal Dialogs Across Thread Boundaries

A common requirement in power testing is prompting the operator for manual actions (e.g. *"Verify oscilloscope probe connections"* or *"Toggle unit switch"*).

Showing a modal `QMessageBox` directly inside the worker thread causes Qt warnings and crashes. Conversely, simply emitting an asynchronous signal causes the worker to continue running before the operator confirms.

PI ATE uses a **Cross-Thread Synchronization Handshake**:

```
 Worker Thread (QThread)                         Main Thread (GUI)
          |                                              |
          | --- 1. emit message(title, text) ----------> |
          |                                              | (QueuedConnection)
          |                                              v
          |                                   2. popup_message() Slot
          |                                      - Calls parent.msg_box_info()
          |                                      - Shows modal QMessageBox (blocks UI)
          |                                              |
          | 3. while not self.message_closed:            |
          |        sleep(0.5)                            |
          |        check abort flags                     |
          |                                              |
          |                                   4. User clicks "OK"
          |                                      - msg_box_info returns
          |                                      - Sets worker.message_closed = True
          |                                              |
          | <--------------------------------------------+
          | 
          | 5. Loop exits (message_closed == True)
          |    Resets message_closed = False
          |    Resumes testing
          v
```

### Code Implementation

**1. Worker Thread Side (`psu_tests/test_vds_ids_steady_state.py`):**
```python
def create_message_popup(self, title: str, message: str, message_type: MessageType):
    if getattr(self, '_auto_confirm_prompts', False):
        return  # Automated test runner bypass
        
    self.message.emit(title, message, message_type)
    
    # Block worker execution until GUI thread signals confirmation
    while not self.message_closed:
        sleep(0.5)
        if test_control_flags.get('StopTest', False):
            raise TestStopped
        if test_control_flags.get('SkipTest', False):
            raise TestSkipped
            
    self.message_closed = False
```

**2. Main Thread Side (`psu_tests/tests.py`):**
```python
@Slot(str, str, MessageType)
def popup_message(self, title: str = '', message: str = '', message_type: MessageType = MessageType.INFO):
    # Executed strictly on the main thread
    self.parent.msg_box_info(title, message, message_type)
    # Unlock worker thread loop
    self.worker.message_closed = True
```

---

## 6. Cooperative Abort & Thread Termination Protocol

### Why Hard Termination (`terminate()`) is Prohibited

Calling `QThread.terminate()` forces the operating system to abort the thread at an arbitrary instruction. In hardware automation, this has catastrophic consequences:
- VISA instrument sessions remain locked, requiring hardware power-cycling.
- AC power sources or electronic loads may remain energized at high voltage/current.
- Open file handles (such as `.xlsx` reports) are corrupted.

### The Cooperative Abort Mechanism

PI ATE implements a safe, cooperative cancellation protocol using a shared dictionary `test_control_flags`:

```python
# Global flag shared across modules
test_control_flags = {
    'StopTest': False,
    'SkipTest': False
}
```

#### Step 1: User Clicks Stop (`page_controls/add_test.py`)
```python
def stop_tests(self):
    if not self.test_plan_update_timer.isActive():
        return

    # 1. Stop the orchestrator timer
    self.test_plan_update_timer.stop()
    
    # 2. Raise cooperative stop flag
    global test_control_flags
    test_control_flags['StopTest'] = True

    # 3. Mark items as STOPPED
    for test_item in self.test_plan.test_items:
        if test_item.status in [TestStatus.IN_PROGRESS, TestStatus.IN_QUEUE]:
            test_item.status = TestStatus.STOPPED
            test_item.test_object.status = TestStatus.STOPPED
    self.test_plan.status = TestStatus.STOPPED
    
    # 4. Gracefully signal thread event loop to exit
    if self.test_routine_thread is not None and self.test_routine_thread.isRunning():
        self.test_routine_thread.quit()
```

#### Step 2: Worker Detects Flag and Executes Safe Teardown
Within the worker's sweep loops, the flag is evaluated before every instrument change:

```python
# Inside test_loop():
for iout_index, iout_level in enumerate(self.iout_list_A):
    if test_control_flags.get('StopTest', False):
        raise TestStopped
    if test_control_flags.get('SkipTest', False):
        raise TestSkipped
```

The exception is caught in `run()`, triggering safe instrument de-energization and report saving:

```python
def run(self):
    try:
        self.setup_equipment()
        self.test_loop()
        self.status_update.emit(TestStatus.COMPLETE)
    except TestStopped:
        # Turn off outputs immediately
        try:
            self.electronic_load.turn_off()
            self.input_supply.turn_off()
        except Exception:
            pass
        self.status_update.emit(TestStatus.STOPPED)
    except Exception as e:
        self.status_update.emit(TestStatus.FAILED)
```

#### Step 3: Thread Cleanup
When `self.status_update` emits `TestStatus.STOPPED` or `TestStatus.COMPLETE`, `TestItem.update_object_status` signals `self.test_routine_thread.quit()`:

```python
@Slot(TestStatus)
def update_object_status(self, status):
    self.test_object.status = status
    if status == TestStatus.COMPLETE:
        self.test_routine_thread.quit()
    elif status == TestStatus.STOPPED:
        self.test_routine_thread.exit(1)
    elif status == TestStatus.FAILED:
        self.test_routine_thread.exit(-1)
```

Once the thread finishes execution, the `finished` signal invokes `deleteLater()` to safely free the underlying C++ Qt thread resources:

```python
def update_status(self):
    def item_status():
        self.test_routine_thread = None
        self.status = self.test_object.status    

    if self.test_object.status not in [TestStatus.IN_PROGRESS, TestStatus.IN_QUEUE]:
        self.test_routine_thread.deleteLater()
    
    QTimer.singleShot(1000, item_status)
```

---

## 7. Other Threaded Subsystems in PI ATE

Beyond main test plan execution, other parts of PI ATE utilize dedicated worker threads:

### A. USB-PD Source Capabilities Discovery (`GetSourceCapsWorker`)
Querying USB-PD Power Data Objects (PDOs) involves synchronizing an AC source ramp with Cypress or STM32 EPR hardware sink negotiation over USB.

Located in `page_controls/add_test.py`:
```python
class GetSourceCapsWorker(QObject):
    failed = Signal()
    finished = Signal()
    state = Signal(str)
    received_caps = Signal(list)

    def __init__(self, ac_source, usbpd_sink, electronic_load):
        super().__init__()
        self.ac_source = ac_source
        self.usbpd_sink = usbpd_sink
        self.electronic_load = electronic_load

    def run(self):
        # Sweeps AC voltage and queries sink controller for advertised PDOs
        ...
```
Invocation:
```python
self.get_source_caps_thread = QThread()
self.get_source_caps_worker = GetSourceCapsWorker(self.ac_source, self.usbpd_sink, self.electronic_load)
self.get_source_caps_worker.moveToThread(self.get_source_caps_thread)

self.get_source_caps_thread.started.connect(self.get_source_caps_worker.run)
self.get_source_caps_worker.received_caps.connect(self.receive_source_caps)
self.get_source_caps_worker.finished.connect(self.source_caps_worker_done)
self.get_source_caps_thread.finished.connect(self.source_caps_thread_cleanup)

self.get_source_caps_thread.start()
```

### B. Augmented PPS Keep-Alive (`sink_controllers/epr_sink_control.py`)
USB-PD Programmable Power Supply (PPS) contracts require continuous keep-alive heartbeats every 10–15 seconds to prevent the power supply from falling back to default 5V. 
- Implemented using dedicated background threads (`self.pps_request_thread = QThread()`) to send periodic ping packets while other tests or measurements execute.

### C. I2C Bus Operations (`page_controls/i2c_controls.py`)
Multi-byte block register reads/writes over CP2112 SMBus bridges run via `self.i2c_command_thread = QThread()` to ensure that high-frequency register polling does not stutter the GUI charts.

---

## 8. Summary Checklist for Writing Thread-Safe Tests

When creating or modifying test routines in PI ATE:

1. **Inherit from `BaseTestObject`**: Always subclass `BaseTestObject` (or `TemplateTest`) which inherits from `QObject`.
2. **Never Touch GUI Widgets**: Do not import or call methods on `QWidget`, `QLineEdit`, or `QTableWidget` inside your test routine. Use `Signal` emissions (`test_data_update`, `progress`, etc.).
3. **Check Abort Flags in Loops**: At the top of every line/load loop iteration, check:
   ```python
   if test_control_flags.get('StopTest', False):
       raise TestStopped
   ```
4. **Wrap Critical Teardown in `try...finally` or `except`**: Ensure power supplies and loads are de-energized even if an unexpected exception occurs.
5. **Use `create_message_popup` for Operator Prompts**: Never call `QMessageBox.exec_()` directly inside a test routine; use the thread-safe `create_message_popup()` helper.
