
import time
import network
import urequests
from machine import Pin, I2C, ADC

# Imports for wifi
import config
import wifi_utils


from dht12 import DHT12    # Temperature and humidity senor
from sh1106 import SH1106_I2C  # Display

# Imports from our subprograms
from TandH import analyze_T, analyze_H
from CO2 import analyze_CO2
from particule import analyze_Particule

# Variables

DISPLAY_WAIT_TIME = 3 # Time to show each sensor screen

# Function to separate the text display in different lines
def oled_multiline(display, text, x=0, y=0, max_chars=16, line_gap=12):
    words = text.split()
    line = ""
    y_offset = y

    for word in words:
        if len(line + word) > max_chars:
            display.text(line, x, y_offset, 1)
            y_offset += line_gap
            line = word + " "
        else:
            line += word + " "

    display.text(line, x, y_offset, 1)

# Hardware initialization
print("Initializing hardware...")

# Define the LEDs
led_g_pin = Pin(25, Pin.OUT)   # Green LED
led_y_pin = Pin(26, Pin.OUT)   # Yellow LED
led_r_pin = Pin(27, Pin.OUT)   # Red LED

# Function to turn off all the LEDs at the same time
def turn_off_leds():
    led_g_pin.off()
    led_y_pin.off()
    led_r_pin.off()

# Initialization of the LEDs
turn_off_leds()
led_g_pin.on()
print("- LEDs initialized (Green ON).")

# Define and inizialize the LEDs
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)
display = SH1106_I2C(i2c)
print("- Display initialized.")

# Definition of the sensors
dht_sensor_obj = DHT12(i2c)

adc_co2 = ADC(Pin(36))
adc_co2.atten(ADC.ATTN_11DB)
adc_co2.width(ADC.WIDTH_12BIT)

adc_particles = ADC(Pin(39))
adc_particles.atten(ADC.ATTN_11DB)
adc_particles.width(ADC.WIDTH_12BIT)
led_particles_control = Pin(4, Pin.OUT)

print("- Sensors initialized.")
time.sleep(1)

# WiFi and cloud set up
wifi = network.WLAN(network.STA_IF)
print("Wi-Fi interface ready.")

def send_to_cloud_thingspeak(data_dict):
    url = f"{config.API_URL}?api_key={config.THINGSPEAK_API_KEY}&field1={data_dict['temperature']}&field2={data_dict['humidity']}&field3={data_dict['co2_proxy_volts']}&field4={data_dict['particles_volts']}&field5={data_dict['status']}"
    print(f"[Cloud] Sending GET request to ThingSpeak...")
    try:
        response = urequests.get(url, timeout=10)
        print(f"[Cloud] Response text (Entry ID): {response.text}")
        response.close()
        return True
    except Exception as e:
        print(f"[Cloud] GET Failed: {e}")
        return False

# Main program (measurements, LEDs and show on the display)
print("\nStarting main measurement loop. Press Ctrl+C to stop.")

try:
    while True:
        print("\n===== New Cycle Started =====")

        # Sensors read the values
        T_data = analyze_T(dht_sensor_obj)
        time.sleep(2)
        H_data = analyze_H(dht_sensor_obj)
        CO2_data = analyze_CO2(adc_co2)
        PM_data = analyze_Particule(adc_particles, led_particles_control)

        # Set which LED is going to switch on depending on the status
        turn_off_leds()
        global_status_str = "IDEAL"
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

        # Show the values and the messages in the displays

        # Temperature
        display.fill(0)   # Reset the text of the diplay
        val = f"{T_data[0]:.1f}" if T_data[0] is not None else "Error"
        display.text(f"Temp: {val} C", 0, 0, 1)     # Show on the display
        oled_multiline(display, T_data[1], 0, 15)
        display.show()
        time.sleep(DISPLAY_WAIT_TIME)

        # Humidity
        display.fill(0)
        val = f"{H_data[0]:.1f}" if H_data[0] is not None else "Error"
        display.text(f"Hum: {val} %", 0, 0, 1)
        oled_multiline(display, H_data[1], 0, 15)
        display.show()
        time.sleep(DISPLAY_WAIT_TIME)

        # CO2
        display.fill(0)
        display.text(f"CO2 Proxy:", 0, 0, 1)
        display.text(f"{CO2_data[0]:.2f} V", 0, 15, 1)
        oled_multiline(display, CO2_data[1], 0, 35)
        display.show()
        time.sleep(DISPLAY_WAIT_TIME)

        # Particules
        display.fill(0)
        display.text(f"Particles:", 0, 0, 1)
        display.text(f"{PM_data[0]:.2f} V", 0, 15, 1)
        oled_multiline(display, PM_data[1], 0, 35)
        display.show()
        time.sleep(DISPLAY_WAIT_TIME)

        # Send data to the cloud
        if T_data[3] == 0 and H_data[3] == 0:
            print("Sensors OK. Preparing cloud transmission...")
            connected = wifi_utils.connect(wifi, config.WIFI_SSID, config.WIFI_PASSWORD)
            if connected:
                data_payload = {
                    "temperature": T_data[0],
                    "humidity": H_data[0],
                    "co2_proxy_volts": CO2_data[0],
                    "particles_volts": PM_data[0],
                    "status": global_status_str
                }
                send_to_cloud_thingspeak(data_payload)
                wifi_utils.disconnect(wifi)
            else:
                print("[Cloud] Skip: Wi-Fi connection failed this cycle.")
        else:
            print("[Cloud] SKIP: Sensor error detected in T or H data.")

        # Switch off the LEDs at the end of eaach cycle
        print("Cycle finished. LEDs OFF.")
        turn_off_leds()
        time.sleep(1)

except KeyboardInterrupt:
    print("\nProgram stopped by user.")
    turn_off_leds()
    display.fill(0)
    display.text("Stopped.", 0, 0, 1)
    display.show()
    wifi_utils.disconnect(wifi)
