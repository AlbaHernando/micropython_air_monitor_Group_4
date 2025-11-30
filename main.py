# ==============================================================================
# MAIN PROGRAM: Indoor Air Quality Monitor (FINAL LAB VERSION)
# ==============================================================================
# Coordinates sensors, displays data sequentially, indicates status via LEDs,
# and transmits data to cloud using connect-send-disconnect cycle per loop.
# ==============================================================================

import time
import network    # For Wi-Fi interface management
import urequests  # For HTTP requests
from machine import Pin, I2C, ADC

# --- IMPORT CONFIGURATION & UTILITIES ---
import config       # Credentials and URL
import wifi_utils   # Wi-Fi helpers from lib/wifi_utils.py

# --- IMPORT HARDWARE DRIVERS ---
from dht12 import DHT12
from sh1106 import SH1106_I2C

# --- IMPORT SENSOR ANALYSIS LOGIC ---
from TandH import analyze_T, analyze_H
from CO2 import analyze_CO2
from particule import analyze_Particule

# --- CONSTANTS ---
DISPLAY_WAIT_TIME = 3 # Time to show each sensor screen

# ==============================================================================
# 1. HARDWARE INITIALIZATION (SETUP)
# ==============================================================================
print("Initializing hardware...")

# --- A. Status LEDs ---
# Define LED pins directly here
led_g_pin = Pin(25, Pin.OUT) # Green LED on GPIO 25
led_y_pin = Pin(26, Pin.OUT) # Yellow LED on GPIO 26
led_r_pin = Pin(27, Pin.OUT) # Red LED on GPIO 27

def turn_off_leds():
    """Helper to turn off all traffic light LEDs."""
    led_g_pin.off(); led_y_pin.off(); led_r_pin.off()

# Initial State: Green ON to indicate power.
turn_off_leds()
led_g_pin.on()
print("- LEDs initialized (Green ON).")

# --- B. I2C Bus & OLED Display ---
# Define I2C pins directly here (SCL=22, SDA=21)
i2c_bus = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)
try:
    display = SH1106_I2C(128, 64, i2c_bus, None, 0x3c)
    display.fill(0); display.text("System Init...", 0, 0, 1); display.show()
    print("- Display initialized.")
except Exception as e:
    print(f"- Display Critical Error: {e}")
    # If display fails, we continue anyway, but show error on console

# --- C. Sensor Objects ---
# 1. DHT12 (Temp/Hum) on shared I2C bus
dht_sensor_obj = DHT12(i2c_bus)

# 2. MQ-135 (CO2 Proxy) on ADC Pin 36 (A0)
# IMPORTANT: Using Pin 36 (VP) for analog input A0.
adc_co2 = ADC(Pin(36))
adc_co2.atten(ADC.ATTN_11DB) # Full range 3.3V
adc_co2.width(ADC.WIDTH_12BIT)

# 3. Particle Sensor on ADC Pin 39 & LED Pin 15
# IMPORTANT: Using Pin 39 (VN) for analog input Vo.
adc_particles = ADC(Pin(39))
adc_particles.atten(ADC.ATTN_11DB)
adc_particles.width(ADC.WIDTH_12BIT)
led_particles_control = Pin(15, Pin.OUT) # LED control on GPIO 15

print("- Sensors initialized.")
time.sleep(1) # Allow sensors to stabilize

# ==============================================================================
# 2. WI-FI & CLOUD SETUP
# ==============================================================================

# Create the Station interface object once
wifi = network.WLAN(network.STA_IF)
print("Wi-Fi interface ready.")

def send_to_cloud_thingspeak(data_dict):
    """
    Sends data to ThingSpeak using a GET request.
    Requires config.API_URL and config.THINGSPEAK_API_KEY to be set.
    """
    # Field mapping: T=field1, H=field2, CO2=field3, Particles=field4, Status=field5
    url = f"{config.API_URL}?api_key={config.THINGSPEAK_API_KEY}&field1={data_dict['temperature']}&field2={data_dict['humidity']}&field3={data_dict['co2_proxy_volts']}&field4={data_dict['particles_volts']}&field5={data_dict['status']}"
    
    print(f"[Cloud] Sending GET request to ThingSpeak...")
    try:
        # Set a timeout for the request to avoid blocking forever
        response = urequests.get(url, timeout=10)
        print(f"[Cloud] Response text (Entry ID): {response.text}")
        response.close() # Always close the connection
        return True
    except Exception as e:
        print(f"[Cloud] GET Failed: {e}")
        return False


# ==============================================================================
# 3. MAIN LOOP
# ==============================================================================
print("\nStarting main measurement loop. Press Ctrl+C to stop.")

try:
    while True:
        print("\n===== New Cycle Started =====")

        # --- STEP 1: READ SENSORS ---
        # Returns: [Value, StatusMsg, GreenFlag, YellowFlag, RedFlag]
        T_data = analyze_T(dht_sensor_obj)
        H_data = analyze_H(dht_sensor_obj)
        CO2_data = analyze_CO2(adc_co2)
        PM_data = analyze_Particule(adc_particles, led_particles_control)


        # --- STEP 2: DETERMINE GLOBAL STATUS & SET LED ---
        turn_off_leds()
        global_status_str = "IDEAL"

        # Priority: Red > Yellow > Green
        if T_data[4] or H_data[4] or CO2_data[4] or PM_data[4]:
            led_r_pin.on()
            global_status_str = "DANGER"
        elif T_data[3] or H_data[3] or CO2_data[3] or PM_data[3]:
            led_y_pin.on()
            global_status_str = "WARNING"
        else:
            led_g_pin.on()
            global_status_str = "IDEAL"
        
        print(f"Global Status: {global_status_str}")


        # --- STEP 3: UPDATE DISPLAY SEQUENTIALLY ---
        # Show data while the status LED remains ON.

        # 3A. Temperature
        display.fill(0)
        val = f"{T_data[0]:.1f}" if T_data[0] is not None else "Error"
        display.text(f"Temp: {val} C", 0, 0, 1)
        display.text(T_data[1], 0, 20, 1)
        display.show()
        time.sleep(DISPLAY_WAIT_TIME)

        # 3B. Humidity
        display.fill(0)
        val = f"{H_data[0]:.1f}" if H_data[0] is not None else "Error"
        display.text(f"Hum: {val} %", 0, 0, 1)
        display.text(H_data[1], 0, 20, 1)
        display.show()
        time.sleep(DISPLAY_WAIT_TIME)

        # 3C. CO2 Proxy
        display.fill(0)
        display.text(f"CO2 Proxy:", 0, 0, 1)
        display.text(f"{CO2_data[0]:.2f} V", 0, 15, 1)
        display.text(CO2_data[1], 0, 35, 1)
        display.show()
        time.sleep(DISPLAY_WAIT_TIME)

        # 3D. Particles
        display.fill(0)
        display.text(f"Particles:", 0, 0, 1)
        display.text(f"{PM_data[0]:.2f} V", 0, 15, 1)
        display.text(PM_data[1], 0, 35, 1)
        display.show()
        time.sleep(DISPLAY_WAIT_TIME)


        # --- STEP 4: CLOUD TRANSMISSION (CYCLE STRATEGY) ---
        # Connect -> Send -> Disconnect
        
        # Safety filter: Only send if T and H sensors are OK (Yellow flag is 0)
        # We don't want to send "None" values to ThingSpeak.
        if T_data[3] == 0 and H_data[3] == 0:
            print("Sensors OK. Preparing cloud transmission...")
            
            # A. Connect using credentials from config
            # (Using the helper function from lib/wifi_utils.py)
            connected = wifi_utils.connect(wifi, config.WIFI_SSID, config.WIFI_PASSWORD)
            
            if connected:
                # B. Create payload data dictionary
                data_payload = {
                    "temperature": T_data[0],
                    "humidity": H_data[0],
                    "co2_proxy_volts": CO2_data[0],
                    "particles_volts": PM_data[0],
                    "status": global_status_str
                }
                # Send to ThingSpeak using the specific function
                send_to_cloud_thingspeak(data_payload)
                
                # C. Disconnect to save power
                wifi_utils.disconnect(wifi)
            else:
                print("[Cloud] Skip: Wi-Fi connection failed this cycle.")
                
        else:
            print("[Cloud] SKIP: Sensor error detected in T or H data.")


        # --- STEP 5: CYCLE FINISH ---
        print("Cycle finished. LEDs OFF.")
        turn_off_leds()
        time.sleep(1) # Short delay before next loop

except KeyboardInterrupt:
    print("\nProgram stopped by user.")
    turn_off_leds()
    display.fill(0); display.text("Stopped.", 0, 0, 1); display.show()
    wifi_utils.disconnect(wifi) # Ensure Wi-Fi is off