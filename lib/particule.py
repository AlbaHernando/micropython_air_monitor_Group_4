import time

# Thresholds (Voltage based)
P_ideal_max = 0.7; P_danger_min = 1.5

def analyze_Particule(adc_obj, led_pin):
    # Hardware specific timing sequence
    led_pin.value(1)
    time.sleep_us(280)
    adc_raw = adc_obj.read()
    time.sleep_us(40)
    led_pin.value(0)
    
    voltage = adc_raw * (3.3 / 4095.0)
    LG=0; LY=0; LR=0; St="Unknown"

    if voltage < P_danger_min:
        if voltage > P_ideal_max: St="Warning: Ventilation recommended"; LY=1
        else: St="Clean air (particles)"; LG=1
    else: St="DANGER: High particle count"; LR=1

    return [voltage, St, LG, LY, LR]