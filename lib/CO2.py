# Variables
CO2_ideal_max_volt = 3  # Below this is Ideal (Green)
CO2_danger_min_volt = 5  # Above this is Danger (Red)


# Function to read CO2 value
def analyze_CO2(adc_object):
    
    # Convert ADC to voltage
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