# --- Configuration Variables ---
# Thresholds based on voltage (approx 0.0V to 3.3V). Empirically determined.
CO2_ideal_max_volt = 0.8   # Below this is Ideal (Green)
CO2_danger_min_volt = 1.5  # Above this is Danger (Red)

def analyze_CO2(adc_object):
    """Read analog voltage from MQ-135 (A0), determine status."""
    # Read raw ADC (0-4095) and convert to voltage
    adc_raw = adc_object.read()
    voltage = adc_raw * (3.3 / 4095.0)

    Led_G = 0; Led_Y = 0; Led_R = 0
    Status = "Unknown"

    if voltage < CO2_danger_min_volt:
        if voltage > CO2_ideal_max_volt:
            Status = "Caution: Air quality fair"; Led_Y = 1
        else:
            Status = "Ideal air quality"; Led_G = 1
    else:
        Status = "DANGER: Poor air quality"; Led_R = 1

    return [voltage, Status, Led_G, Led_Y, Led_R]