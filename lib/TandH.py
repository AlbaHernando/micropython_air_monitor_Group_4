import time

# --- Configuration Variables ---
# Temperature thresholds (Celsius)
Last_T = 25.0          # Initial memory value
T_Phys_Max = 80.0      # Absolute physical max
T_Phys_Min = -30.0     # Absolute physical min
Max_Change_T = 2.0     # Max allowed change (spike filter)
T_Max = 24.0           # Upper limit for ideal range
T_Min = 20.0           # Lower limit for ideal range

# Humidity thresholds (%)
Last_H = 50.0          # Initial memory value
H_Phys_Max = 100.0     # Absolute physical max
H_Phys_Min = 0.0       # Absolute physical min
Max_Change_H = 5.0     # Max allowed change (spike filter)
H_Max = 60.0           # Upper limit for healthy range
H_Min = 40.0           # Lower limit for healthy range


def analyze_T(dht_sensor_obj):
    """Read and analyze Temperature from DHT12 object."""
    global Last_T
    try:
        T, H = dht_sensor_obj.read_values()
    except Exception as e:
        # If sensor fails to read, return error state
        return [None, "Sensor Read Error", 0, 1, 0]

    Led_G_T = 0
    Led_Y_T = 0
    Led_R_T = 0
    Status_T = "Unknown"

    # 1. Physical Range Check
    if T_Phys_Min < T < T_Phys_Max:
        
        # 2. Spike Check
        if abs(T - Last_T) < Max_Change_T:
            Last_T = T  # Update memory
            
            # 3. Health/Comfort Range Check
            if T_Min <= T <= T_Max:
                Status_T = "Ideal Temperature"
                Led_G_T = 1
            else:
                if T > T_Max:
                    Status_T = "Temp too high"
                else:
                    Status_T = "Temp too low"
                Led_R_T = 1
        else:
            # Spike detected
            Status_T = "Ignored spike error"
            Led_Y_T = 1
            T = Last_T # Keep last good value
            
    else:
        # Physical range error
        Status_T = "Physical sensor error"
        Led_Y_T = 1
        T = Last_T # Keep last good value

    return [T, Status_T, Led_G_T, Led_Y_T, Led_R_T]


def analyze_H(dht_sensor_obj):
    """Read and analyze Humidity from DHT12 object."""
    global Last_H
    try:
        T, H = dht_sensor_obj.read_values()
    except Exception as e:
         return [None, "Sensor Read Error", 0, 1, 0]

    Led_G_H = 0
    Led_Y_H = 0
    Led_R_H = 0
    Status_H = "Unknown"

    # 1. Physical Range Check
    if H_Phys_Min < H < H_Phys_Max:
        
        # 2. Spike Check
        if abs(H - Last_H) < Max_Change_H:
            Last_H = H # Update memory

            # 3. Health Range Check
            if H_Min <= H <= H_Max:
                Status_H = "Ideal Humidity"
                Led_G_H = 1
            else:
                if H > H_Max:
                    Status_H = "Humidity too high"
                else:
                    Status_H = "Humidity too low"
                Led_R_H = 1
        else:
            Status_H = "Ignored spike error"
            Led_Y_H = 1
            H = Last_H
            
    else:
        Status_H = "Physical sensor error"
        Led_Y_H = 1
        H = Last_H
        
    return [H, Status_H, Led_G_H, Led_Y_H, Led_R_H]