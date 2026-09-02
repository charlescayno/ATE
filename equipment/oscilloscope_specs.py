import os

import uuid
           
from lecroydso import LeCroyDSO

from equipment.equipment import Equipment

class TriggerMode:
    AUTO = "Auto"
    NORMAL = "Normal"
    FREERUN = "Freerun"
    STOPPED = "Stopped"

class OscilloscopeBaseClass(Equipment):
    def __init__(self, device, device_id):
        print("Scope Creation")
        super().__init__(device, device_id)
        print("Scope created")
    # TODO: Limit the methods common to all oscilloscope classes
    # Implementation will be very different between manufacturers
    # So just use a few common methods first

    def set_default_setup(self):
        pass

    def setup_ripple(self, y_scale=0.05):
        pass

    def get_screenshot(self, filename, path):
        pass

    def get_measure(self, param):
        pass

    # This ends the common methods

    def channel_settings(self):
        pass


    def add_zoom(self):
        pass

    def remove_zoom(self):
        pass

    def measure(self):
        pass

    def record_length(self):
        pass

    def time_position(self):
        pass

    def time_scale(self):
        pass

    def set_trigger_mode(self):
        pass

    def run(self):
        pass
    
    def run_single(self):
        pass
    
    def stop(self):
        pass

class RohdeSchwarzOscilloscope(OscilloscopeBaseClass):
    def __init__(self, device, device_id):
        super().__init__(device, device_id)

    def channel_settings(self, state, channel=1, scale=1, position=0, label='IOUT', color='LIGHT_BLUE', rel_x_position=50, rel_y_position=50, bandwidth=500, coupling='DCLimit', offset=0):
        """
        COLOR OPTIONS:

        - LIGHT_BLUE
        - YELLOW
        - PINK
        - GREEN
        - BLUE
        - ORANGE


        returns : state of the channel ('ON' or 'OFF')
        """

        self.channel_state(channel, state)

        self.channel_position(channel, position)
        self.channel_scale(channel, scale)
        
        #if state == 'ON': print(f"CH{channel} - {label}")
        self.channel_label(channel, label, rel_x_position,rel_y_position)
        self.channel_color(channel, color)

        self.channel_BW(channel, bandwidth)
        
        self.channel_coupling(channel, coupling)
        self.channel_offset(channel, offset)
        
        self.display_intensity()

        self.measure_enable(channel, state)

        return state

    def get_measure(self, channel=1):
        channel_state = self.write(f'MEAS{channel}:ENAB?')
        if channel_state == '0':
            return None, None
        
        labels = []
        values = []
        self.write(f'MEAS{channel}:ARN ON')

        for item in self.write(f'MEAS{channel}:ARES?').split(','):
            label, value = item.split(':')
            labels.append(label.strip())
            values.append(float(value.strip()))  
        
        return values[0]

    def get_screenshot(
            self, 
            filename="default.png", 
            path=os.path.dirname(os.path.realpath(__file__))):
        
        def _extract_png(raw):
            offset = int(raw[1])-ord('0')
            return raw[offset+2:]
        
        self.device.timeout = 5000
        self.write("HCOP:DEST \'MMEM\'")
        self.write("HCOP:DEV:LANG PNG")
        self.write("HCOP:DEV:INV ON")
        self.write("MMEM:NAME \'C:\\HCOPY.png\'")
        self.write("HCOP:IMMediate; *OPC?")

        self.device.write("MMEM:DATA? \'C:\\HCOPY.png\'")
        raw_image = self.device.read_raw()
        image = _extract_png(raw_image)

        with open(path + "\\" + filename, "wb") as f:
            f.write(image)

    def setup_ripple(self, y_scale=0.1, channel=1):
        self.hide_all_channels()
        self.show_channel(channel)
        self.add_zoom()
        self.set_vertical(channel, scale=y_scale, offset=0, pos=0)
        self.set_horizontal(scale=0.005, offset=0, position=0)
        self.set_trigger_mode(TriggerMode.AUTO)
        self.hide_measurements()
        self.clear_measure(channel)
        self.channel_coupling(channel, 'AC')
        self.measure(channel=channel, measure='PDELTA')
        self.record_length(50E6)
        self.run()
    
    def hide_all_channels(self):
        for channel in [1,2,3,4]:
            self.hide_channel(channel)

    def hide_channel(self, channel):
        self.write(f"CHANnel{channel}:STATe OFF")

    def show_channel(self, channel):
        self.write(f"CHANnel{channel}:STATe ON")

    def add_zoom(self, rel_pos=0, rel_scale=25, vert_scale=100):
        self.remove_zoom()
        for i in range(5):
            self.write(f"LAYout:ZOOM:ADD 'Diagram{i}', VERT, OFF, -100e-6, 100e-6, 0, 5, 'Zoom1'")
            self.write(f"LAYout:ZOOM:HORZ:REL:SPAN 'Diagram{i}', 'Zoom1', {rel_scale}")
            self.write(f"LAYout:ZOOM:HORZ:REL:POS 'Diagram{i}', 'Zoom1', {rel_pos}")
            self.write(f"LAYout:ZOOM:VERT:REL:SPAN 'Diagram{i}', 'Zoom1', {vert_scale}")

            # Create an new zoom diagram for Diagram{i}
            self.write(f"LAYout:ZOOM:ADD 'Diagram{i}', VERT, OFF, -10e-9, 20e-9, -0.5, 0.5, 'MyZoom1'")
            # Set horizontal zoom mode to relative
            self.write(f"LAYout:ZOOM:HORZ:MODE 'Diagram{i}', 'MyZoom1', REL")     
            # Set horizontal zoom span in percent
            self.write(f"LAYout:ZOOM:HORZ:REL:SPAN 'Diagram{i}', 'MyZoom1', 10")
            # Set horizontal zoom position in percent
            self.write(f"LAYout:ZOOM:HORZ:REL:POS 'Diagram{i}', 'MyZoom1', 15")
            self.write("*OPC?") 
            # // Remove zoom diagram
            # self.write(f"LAYout:ZOOM:REM 'Diagram1', 'MyZoom1'        
            self.write("*OPC?")


    def remove_zoom(self):
        self.write("LAYout:ZOOM:REM 'Diagram1', 'Zoom1'")
        self.write("LAYout:ZOOM:REM 'Diagram1', 'Zoom2'")

    def set_vertical(self, channel, scale=None, offset=None, pos=None):
        channel_state = self.write(f'CHAN{channel}:STAT?')
        if channel_state == '0':
            return None
        if scale is not None:
            self.write(f'CHAN{channel}:SCAL {scale}') # V/div

        if offset is not None:
            self.write(f'CHAN{channel}:OFFS {offset}') # V
    
        if pos is not None:
            self.write(f'CHAN{channel}:POS {pos}') # V

    def set_horizontal(self, scale=None, offset=None, position=None):
        if offset is not None:
            self.write(f'TIM:REF {offset}')
            self.write('TIM:HOR:POS 0')
        if scale is not None:
            self.write(f'TIM:SCAL {scale}')

        if position is not None:
            self.write(f'TIM:REF {position}')

    def set_trigger_mode(self, mode):
        self.write(f'TRIG:MODE {mode}') # AUTO | NORMal | FREerun

    def hide_measurements(self):
        for channel in [1,2,3,4]:
            self.write(f"MEASurement{channel}:ENABle OFF")
        
    def measure(self, channel:int, measure:str):
        """
        HIGH | LOW | AMPLitude | MAXimum | MINimum | PDELta |
        MEAN | RMS | STDDev | POVershoot | NOVershoot | AREA |
        RTIMe | FTIMe | PPULse | NPULse | PERiod | FREQuency |
        PDCYcle | NDCYcle | CYCarea | CYCMean | CYCRms |
        CYCStddev | PULCnt | DELay | PHASe | BWIDth | PSWitching |
        NSWitching | PULSetrain | EDGecount | SHT | SHR | DTOTrigger |
        PROBemeter | SLERising | SLEFalling
        """
        self.measure_source(channel)
        self.measure_off(channel)
        measure_list = measure.strip(" ").split(",")
        for meas_type in measure_list:
            self.write(f"MEASurement{channel}:MAIN {meas_type}")
            self.write(f"MEASurement{channel} ON")
    def measure_enable(self, channel, state='ON'):
        self.write(f"MEASurement{channel}:ENABle {state}")

    def measure_source(self, channel):
        self.write(f"MEASurement{channel}:SOURce C{channel}W1")
        self.write(f"MEASurement{channel}:CATegory AMPTime")
    
    def measure_off(self, channel):
        self.write(f"MEASurement{channel}:AOFF")
    
    def clear_measure(self, channel):
        self.write(f"MEASurement{channel}:CATegory PROT")

    def channel_coupling(self, channel, coupling):
        """
        DC | DCLimit | AC
        """
        channel_state = self.write(f'CHAN{channel}:STAT?')
        if channel_state == '0':
            return None

        self.write(f'CHAN{channel}:COUP {coupling}')
        
    def record_length(self, record_length):
        """
            record_length : 1000 to 1 000 000 000
        """
        self.write(f'ACQ:POIN {record_length}')

    def time_position(self):
        pass

    def time_scale(self):
        pass

    def run(self):
        self.write('RUN')
        self.write('DISP:TRIG:LIN OFF')
        
    def run_single(self):
        self.write('RUNS')
        self.write('DISP:TRIG:LIN OFF')

    def stop(self):
        self.write('STOP')
        self.write('DISP:TRIG:LIN OFF')


class LeCroyOscilloscope(OscilloscopeBaseClass):
    device: LeCroyDSO
    def __init__(self, device, device_id):
        super().__init__(device, device_id)

    def channel_settings(self):
        pass

    def get_measure(self, param):
        return self.device.get_measure_value(f'P{param}')

    def get_screenshot(
        self, 
        filename="default.png", 
        path=os.path.dirname(os.path.realpath(__file__))):
        """Get a screenshot from the oscilloscope and save it locally
        """
        req_extension = os.path.splitext(filename)[1]
        local_filepath = os.path.join(path, filename)
        # LeCroy spawns a prompt when the same name is used for the screen image
        # so a UUID is created to avoid spawning one
        remote_filename = str(uuid.uuid4())+req_extension
        remote_folderpath = "C:\\PI_ATE"
        remote_filepath = f"{remote_folderpath}\\{remote_filename}"
        # filename = f"{temp_filename}.jpg"
        self.device.write_vbs(f'app.HardCopy.Directory = "C:\PI_ATE"')
        self.device.set_hardcopy(filename = remote_filename, destination = 'FILE', 
                    area = 'FULLSCREEN', orientation ='LANDSCAPE', color = 'PRINT')
        self.device.write_vbs(f'app.HardCopy.PromptForMessage = False')
        self.hardcopy_print()
        
        # set the device timeout to a long duration before transfer operation
        self.device._conn.timeout = 10
        self.device.transfer_file_to_pc(
            remoteDevice='HDD', 
            remoteFileName=remote_filepath, 
            localFileName=local_filepath)
        
        # reset the device timeout for normal operations
        self.device._conn.timeout = 1

    def add_zoom(self):
        pass

    def remove_zoom(self):
        pass

    def measure(self):
        pass

    def record_length(self):
        pass

    def time_position(self):
        pass

    def time_scale(self):
        pass

    def set_trigger_mode(self, mode):
        """Set the trigger mode of the acquisition
        Modes: Auto, Normal, Single, Stopped"""

        self.device.write_vbs(f"acq.TriggerMode = \"{mode}\"")

        

    def setup_ripple(self, y_scale=0.2):
        """Prepare the scope setup needed for ripple testing."""
        self.device.close_docked_dialog()
        self.set_default_setup()
        self.hide_all_channels()
        self.show_channel('C1',1)
        self.show_zoom(zoom_ch='Z1',show=True, pos=0, scale=25)
        self.set_vertical('C1', scale=y_scale, offset=0)
        self.set_horizontal(scale=0.005, offset=0)
        self.set_trigger_mode(TriggerMode.AUTO)
        self.hide_measurements()
        self.set_channel_coupling('C1', 'AC1M')
        self.set_measure(param='P1', source1='C1', engine='PeakToPeak')
        self.device.set_max_samples(50E6)

    def set_default_setup(self):
        self.device.write_vbs('app.SaveRecall.Setup.DoRecallDefaultPanelWithTriggerModeAuto')
    
    def hide_all_channels(self):
        """Hide all of the channels of the oscilloscope."""
        for channel in self.device.available_channels:
            self.hide_channel(channel)

    def hide_channel(self, channel: str):
        """Hide the specified channel.
        
        Channels: C1-C8
        """
        self.device.write_vbs(f'acq.{channel}.View = False')

    def show_channel(self, channel:str, position=None):
        """Show the channel if it is hidden. 
        If position is specified, move it to that grid
        """
        self.device.write_vbs(f'acq.{channel}.View = True')

        if position is not None:
            self.device.write_vbs(f'acq.{channel}.UseGrid = "YT{position}"')

    def show_zoom(self, zoom_ch, show:bool, pos:float = 0, scale:float = 10):
        """Show or hide the zoom depending on the value of show.
        Args:
        pos:    Sets the center position of the zoom in terms of divisions
                0 corresponds to center, -1 corresponds to 1 division to the left
        scale:  Sets how much zoom. 10 corresponds to 10x zoom or 1/10 of total
                screen area is shown in the zoom
        """
        self.device.show_zoom(zoom_ch, show)
        self.device.write_vbs(f'zoom.{zoom_ch}.Zoom.HorPos = {pos}')
        self.device.write_vbs(f'zoom.{zoom_ch}.Zoom.HorZoom = {scale}')

    def set_vertical(self, channel, scale=None, offset=None):
        """Set the vertical settings of a channel
        
        Args:
        channel: the channel to be set, C1-C8
        scale: scale in volts/div
        offset: offset value in Volts at the vertical center
        """
        if scale is not None:
            self.device.set_ver_scale(channel,scale)

        if offset is not None:
            self.device.set_ver_offset(channel, offset)

    def set_horizontal(self, scale, offset):
        """Set the horizontal settings of the acquisition
        
        Args:
        scale: scale in seconds/div
        offset: offset value in seconds at the horizontal center
        """
        
        if scale is not None:
            self.device.set_hor_scale(scale)
        if offset is not None:
            self.device.set_hor_offset(offset)

    def hide_measurements(self):
        """Hide all of the measurement parameters"""
        for param in self.device.available_parameters:
            if 'P' == param[0] and len(param) == 2:
                self.hide_measurement(param)


    def hide_measurement(self, param):
        """ Hide the measurement specified
        
        Args:
        param:      P1-PX, according to how many is available
        """
        self.device.write_vbs(f'meas.{param}.View = False')

    def set_measure(
            self,
            param, 
            source1, 
            source2='None', 
            engine='PeakToPeak', 
            view=True):
        """Set a measurement with the inputs:
        
        Args:
        param:      Parameter to be set, P1-PX
        source1:    First input to the measurement
        source2:    Second input to the measurement, defaults to 'None'
        engine:     Measurement Type
        view:       Show or hide the measurement, defaults to True"""
        self.device.set_measure(param, source1, source2, engine, view)

    def hardcopy_print(self):
        """Overloaded from the LeCroyDSO object
        Generate a hardcopy
        """
        self.device.write_vbs('app.Hardcopy.Print')

    def set_channel_coupling(self, channel, coupling):
        self.device.set_coupling(channel, coupling)

    def run(self):
        self.set_trigger_mode(TriggerMode.AUTO)

    def run_single(self):
        pass
    
    def stop(self):
        self.set_trigger_mode(TriggerMode.STOPPED)