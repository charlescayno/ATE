from equipment.handler import EquipmentHandler
from time import sleep
import numpy as np

from sink_controllers import pat_tool
pat_tool.FAST_I2C_WRITE = True


class SWEEP_MODE:
    UP      = (True,False)
    DOWN    = (False,True)
    UP_DOWN = (True,True)

def cv_sweep(min, max, step, sweep_mode):
    delta = round(round(min,2)-round(max,2),2)
    n_steps = abs(int(round(delta/round(step,2),2)))
    cv_range = np.round(np.linspace(start = min, stop=max, num=n_steps),1)
    cv_range_rev = np.flip(cv_range)

    if sweep_mode[0]:
        for vout in cv_range[1:]:
            i2c.cv(vout_V=vout, autocv=True)
    if sweep_mode[1]:
        for vout in cv_range_rev[1:]:
            i2c.cv(vout_V=vout, autocv=True)



equipment = EquipmentHandler(None)

ac_source = equipment.ac_source
eload = equipment.electronic_load_1

ac_source.voltage = 115
ac_source.turn_on()

sleep(2)

eload.set_load(iout_A=1, vout_V=6,mode='CC')
eload.turn_off()

sleep(1)

i2c = equipment.i2c_controller
i2c.open()
cmd = i2c.commands

i2c.watchdog(setting=cmd.WATCHDOG_OFF)
i2c.cvo(cvo_en=True, timer=cmd.CVO_TIMER_16MS, response=cmd.CVO_RESP_NR)
i2c.uva(threshold_V=2.7, response=cmd.UVA_RESP_NR, timer=cmd.UVA_TIMER_16MS)
i2c.ova(threshold_V=30, response=cmd.OVA_RESP_NR)
i2c.cv(vout_V=10,autocv=True)
i2c.vben(setting=cmd.VBEN_ON)
i2c.fast_vi(setting=True)
i2c.bleeder(bleeder_en=cmd.BLEEDER_ON_AUTO_DIS, weak_bleeder_en=cmd.WEAK_BLEEDER_ON)
i2c.sr_zvs(delay_time_count=3, on_time_count=3, fwd_valley_switch_en=True, sr_zvs_en=True)
sleep(.020)



cv_sweep(min=3, max=10, step=0.1, sweep_mode=SWEEP_MODE.DOWN)