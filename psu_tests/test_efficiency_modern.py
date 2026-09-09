import time
from psu_tests.modern_base_test_class import ModernBaseTestObject
from data_process.data_pipeline import TestTelemetryLogger
from plotter.plotter import PlotType

class ModernEfficiencyTest(ModernBaseTestObject):
    title = "Efficiency Modern"
    short_title = "Eff_Modern"

    def setup_test(self):
        # 1. Initialize the logger with column headers
        headers = [
            "Vin (VAC)", "Freq (Hz)", "Iout (A)", "Vout (V)", 
            "Pin (W)", "Pout (W)", "Efficiency (%)"
        ]
        self.logger = TestTelemetryLogger(headers=headers)
        
        # 2. Add plots for the real-time UI
        self.logger.add_plot("Efficiency", x_header="Iout (A)", y_headers=["Efficiency (%)"], plot_type=PlotType.LINE_PLOT)
        self.logger.add_plot("Vout", x_header="Iout (A)", y_headers=["Vout (V)"], plot_type=PlotType.LINE_PLOT)

        # 3. Setup excel output (if output_folder_path is provided)
        if hasattr(self, 'output_folder_path') and self.output_folder_path:
            excel_path = f"{self.output_folder_path}/Efficiency_Modern_Output.xlsx"
            self.logger.setup_excel(excel_path)
            
    def execute_sweep(self):
        # Extract conditions (simplified for demonstration)
        line_range = getattr(self.test_conditions, 'line_range', None)
        load_range = getattr(self.test_conditions, 'load_range', None)
        
        # Use dummy lists if not perfectly hooked up to the old UI payload
        vin_list = line_range.vin_freq if line_range and hasattr(line_range, 'vin_freq') else [(115.0, 60.0), (230.0, 50.0)]
        iout_list = load_range.load_range_pct if load_range and hasattr(load_range, 'load_range_pct') else [100.0, 50.0, 25.0, 10.0]
        
        total_points = len(vin_list) * len(iout_list)
        current_point = 0

        for vin, freq in vin_list:
            self.ac_source.set_voltage(vin)
            self.ac_source.set_frequency(freq)
            self.ac_source.turn_on()
            time.sleep(1) # Soak per line

            for load_pct in iout_list:
                # Convert pct to A based on nominal
                iout = (load_pct / 100.0) * getattr(self.test_conditions, 'nominal_load_current_A', 5.0)
                self.electronic_load.set_current(iout)
                self.electronic_load.turn_on()
                time.sleep(0.5) # Soak per load
                
                # Fetch telemetry
                # (Assuming simple mock behavior or actual SCPI commands)
                vout = self.power_meter.get_voltage() if hasattr(self.power_meter, 'get_voltage') else 5.0
                pin = self.power_meter.get_power() if hasattr(self.power_meter, 'get_power') else (vout * iout * 1.1)
                pout = vout * iout
                eff = (pout / pin * 100) if pin > 0 else 0
                
                # Record via the pipeline! One call handles UI, Plotting, and Excel.
                self.logger.record_datapoint({
                    "Vin (VAC)": vin,
                    "Freq (Hz)": freq,
                    "Iout (A)": iout,
                    "Vout (V)": vout,
                    "Pin (W)": pin,
                    "Pout (W)": pout,
                    "Efficiency (%)": eff
                })
                
                # Update UI
                self.test_data_update.emit(self.logger.get_gui_update_payload())
                current_point += 1
                self.progress.emit((current_point / total_points) * 100.0)
                
            self.electronic_load.turn_off()
        
        self.ac_source.turn_off()
