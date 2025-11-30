# ==============================================================================
# Wi-Fi Utilities Library
# ==============================================================================
# Functions for managing Wi-Fi connection
# ==============================================================================

import network
import time

def connect(wlan_interface, ssid, password, timeout_secs=15):
    """
    Connects the provided WLAN to the network.
    
    :param wlan_interface: The network.WLAN(network.STA_IF) object.
    :param ssid: Network name (string).
    :param password: Network password (string).
    :param timeout_secs: Max time to wait for connection (default 15s).
    :return: True if connected successfully, False otherwise.
    """
    if not wlan_interface.isconnected():
        print(f"[WiFi] Connecting to network: {ssid}...")
        wlan_interface.active(True)
        wlan_interface.connect(ssid, password)
        
        start_time = time.time()
        while not wlan_interface.isconnected():
            if time.time() - start_time > timeout_secs:
                print("[WiFi] Connection timed out!")
                wlan_interface.active(False) # Turn off to save power
                return False
            time.sleep(0.5)
            print(".", end="") # Show progress dots
            
    print(f"\n[WiFi] Connected! IP Address: {wlan_interface.ifconfig()[0]}")
    return True

def disconnect(wlan_interface):
    """
    Disconnects the WLAN interface and turns off the radio to save power.
    """
    if wlan_interface.isconnected() or wlan_interface.active():
        print("[WiFi] Disconnecting...")
        wlan_interface.disconnect()
        wlan_interface.active(False)
        print("[WiFi] Disconnected and radio turned off.")