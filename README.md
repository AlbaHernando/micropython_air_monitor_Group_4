## Indoor air quality monitoring system

* [1. Project Overview](#1-project-overview)
* [2. Hardware Components](#2-hardware-components)
* [3. Software description](#3-software-description)
* [4. Instructions and photos](#4-instructions-and-photos)
* [5. References and tools](#5-references-and-tools)

## Project 1: ESP32 Indoor Air Quality Monitor
Course: BPA-DE2 (Digital Electronics) 2025/26 Team Members:

- **Xabier Asla:** Responsible for 
- **Alba Hernando:** Responsible for 
- **Pablo Vicente:** Responsible for 
---
## 1. Project Overview
**Problem Statement**

Indoor Air Quality (IAQ) is a critical factor influencing human health, comfort, and productivity. Pollutants such as particulate matter (PM2.5/PM10), high levels of Carbon Dioxide (CO2), and volatile organic compounds (VOCs) can accumulate in poorly ventilated indoor environments like homes, schools, and offices. Many of these spaces lack real-time, accessible monitoring, leaving occupants unaware of potential health risks.

**Proposed Solution**

This project aims to design and build a cost-effective, real-time Indoor Air Quality monitoring system using an ESP32 FireBeetle microcontroller programmed in MicroPython.

The system will:

1.  **Measure environmental parameters sequentially:** First, it reads the temperature and humidity from the DHT12, then checks the general air quality (CO2 proxy) with the MQ-135, and finally measures particulate matter (PM2.5 & PM10) using the optical sensor.
2.  **Analyze and Determine Status:** The code compares these readings against health thresholds to decide the overall status of the room: **Ideal (Green), Warning (Yellow), or Danger (Red)**.
3.  **Display Data Locally:** It shows the readings and status messages right on the OLED screen for immediate feedback to occupants.
4.  **Visually Alert:** To make it obvious at a glance, it activates physical traffic-light LEDs corresponding to the global status.
5.  **Transmit Data:** Finally, it sends all the collected data via Wi-Fi to a cloud-based dashboard for remote monitoring and historical logging.

---
## 2. Hardware Components

This section details the hardware selected for the prototype, justifications, and the connection scheme.

### 2.1 Component Visual Overview


<table align="center">
  <tr>
    <td align="center" width="33%">
      <img src="https://github.com/user-attachments/assets/3c8842ac-89b0-4d19-9491-1b28500b538d" alt="ESP32 FireBeetle" width="95%">
      <br>
      <em>Main Controller (ESP32 FireBeetle)</em>
    </td>
    <td align="center" width="33%">
      <img src="https://github.com/user-attachments/assets/b87f8879-f5fa-497d-8490-917ca713a047" alt="DHT12 Sensor" width="95%">
      <br>
      <em>Temp & Humidity Sensor (DHT12)</em>
    </td>
    <td align="center" width="33%">
      <img src="https://github.com/user-attachments/assets/158a1572-d56c-4f0d-95f1-2d5a76e697ce" alt="MQ-135 Sensor" width="95%">
      <br>
      <em>Air Quality Proxy Sensor (MQ-135)</em>
    </td>
  </tr>
  
  <tr>
    <td align="center" width="33%">
      <img src="https://github.com/user-attachments/assets/e3ff0a67-f6a2-4fb7-a812-33316e15e527" alt="Particle Sensor" width="95%">
      <br>
      <em>Optical Particle Sensor (GP2Y10)</em>
    </td>
    <td align="center" width="33%">
      <img src="https://github.com/user-attachments/assets/232918aa-34fe-408a-a5ac-71618d92a3c1" alt="OLED Display" width="95%">
      <br>
      <em>OLED Display (0.96" I2C)</em>
    </td>
    <td align="center" width="33%">
      <img src="https://github.com/user-attachments/assets/4cf6bb4f-72ea-4c29-8b47-8cb40cc9ae43" alt="Status LEDs" width="95%">
      <br>
      <em>Status LEDs (Red, Yellow, Green)</em>
    </td>
  </tr>
</table>

<p align="center">
  <em>Figure 1: Selected Hardware Components Overview.</em>
</p>



### 2.2 Component List & Functions

| Component | Type | Primary Role / Function |
| :--- | :--- | :--- |
| **ESP32 FireBeetle** | MCU | Main controller; manages sensors, data processing, and Wi-Fi transmission to the cloud. |
| **DHT12** | Sensor | Measures ambient Temperature and Relative Humidity (digital output). |
| **MQ-135** | Sensor | Detects general air quality gases (VOCs, smoke) acting as a proxy for poor ventilation (analog output). |
| **SDS011** | Sensor | Uses laser scattering to precisely count fine dust particles (PM2.5 & PM10) (UART serial). |
| **OLED Display (0.96")**| Output | Provides immediate real-time visual feedback of readings to occupants (I2C). |
| **Status LEDs** | Output | Red/Yellow/Green traffic-light indicators for quick "at-a-glance" air quality status. |
| **Breadboard & Wires**| Prototyping | Solderless infrastructure for rapid circuit building and testing. |

  
### 2.3 Circuit diagram and wiring

The following diagram shows how all components are connected to the ESP32 FireBeetle microcontroller.

<p align="center">
  <img src="https://github.com/user-attachments/assets/8bb77021-7ce6-46e1-b73e-c4bcd403c7c1" alt="Circuit Wiring Diagram" width="700">
  <br>
  <em>Figure 2: Complete System Wiring Diagram.</em>

  ### Pinout Table (Connection Scheme)


| Component | Component Pin | ESP32 Pin (GPIO) | Function |
| :--- | :--- | :--- | :--- |
| **DHT12 (Temp/Hum)** | SDA | **21** | I2C Data Bus (Shared) |
| | SCL | **22** | I2C Clock Bus (Shared) |
| **OLED Display** | SDA | **21** | I2C Data Bus (Shared) |
| | SCL | **22** | I2C Clock Bus (Shared) |
| **MQ-135 (CO2 Proxy)**| A0 (Analog Out) | **36** (Sensor VP) | Analog Input (ADC) |
| **GP2Y10 (Particles)**| Vo (Analog Out) | **39** (Sensor VN) | Analog Input (ADC) |
| | V-LED (LED Ctrl)| **15** | Digital Output (LED Pulse) |
| **Red LED** | Anode (+) | **27** | Digital Output |
| **Yellow LED** | Anode (+) | **26** | Digital Output |
| **Green LED** | Anode (+) | **25** | Digital Output |
| **Power** | VCC/VDD | 3V3 / 5V | Power Supply |
| **Ground** | GND | GND | Common Ground |
---

## 3. Software description

To make the software easy to manage and understand, we wrote it in MicroPython and organized it using a modular approach.

### 3.1 Project Directory Structure

The source code is organized into a main controller script in the root directory and specific sensor/helper libraries in a `/lib` subdirectory.


```
/ (Root Directory)
│
├── main.py          # The central coordinator script.
├── config.py        # Contains credentials (WiFi SSID/Pass, API URL).
│
└── /lib             # Custom libraries folder
    ├── TandH.py         # Logic for Temperature & Humidity analysis.
    ├── CO2.py           # Logic for MQ-135 reading and analysis.
    ├── particule.py     # Logic for Particle sensor reading sequence.
    ├── wifi_utils.py    # Helper functions for managing Wi-Fi connection.
    ├── dht12.py         # Hardware driver for DHT12 sensor.
    └── sh1106.py        # Hardware driver for OLED display.
```



### 3.2 Overall System Logic Explained

The `main.py` script develops the following sequential loop:

1.  **Initialization:** On startup, the system initializes all hardware pins (I2C, ADCs, LEDs), turns on the Green LED to indicate power, and attempts to connect to Wi-Fi using credentials from `config.py`.
2.  **Measurement Cycle (Step 1):** The system sequentially calls the analysis functions imported from the `/lib` folder (`analyze_T`, `analyze_H`, etc.). Each library function reads its respective hardware sensor, applies threshold logic to determine a status (OK, Warning, Danger), and returns both raw values and status flags.
3.  **Global Status Determination (Step 2):** The main script evaluates the status flags returned by all sensors. It applies a priority logic: **Red (Danger) trumps Yellow (Warning), which trumps Green (Ideal)**. The corresponding physical LED is turned ON.
4.  **Display Update (Step 3):** While the status LED is active, the system iterates through the sensor data, updating the OLED display sequentially with each sensor's readings and status messages, pausing briefly for readability.
5.  **Cloud Transmission (Step 4):** If Wi-Fi is connected, the system packages all collected data and the global status into a JSON payload and sends it via an HTTP POST request to the configured cloud endpoint. *Note: Data sending is skipped if critical sensor errors are detected to maintain data integrity.*
6.  **Repeat:** The LEDs are reset, and after a short delay, the cycle begins anew.



We created a flowchart for each measurement (Temperature, Humidity, CO2 and Particles), and one final flowchard unifiying all the parameters, integrating the function of Wi-Fi and the monitoring of data, being this flowchard the main program. Each of the individual flowchards of the measurements will be a subclass in MicroPython.




*DESCRIPTIONS WITH WIRES AND CONNECTIONS*
### DHT22 Sensor Logic (Temperature & Humidity)

A unified flowchart has been developed for the DHT22 sensor. Since this single hardware component measures both temperature and humidity, combining their logic accurately reflects the sequential reading and processing workflow, optimizing code structure and display output.

<details>
  <summary>▶️ <strong>Click here to expand the Flowchart of sensor DHT12 (Temperature & Humidity)</strong></summary>
  <br>
  <p align="center">
    <img src="https://github.com/user-attachments/assets/b2d0b347-fffe-4892-9014-18a7e2c6da55" alt="DHT12 Combined Flowchart" width="800">
    <br>
    <em>Logic for Temperature and Humidity Sequential Processing</em>
  </p>
</details>


---
## 4. Instructions and photos
Describe how to use the application. Add photos or videos of your application.
---
## 5. References and tools
Put here the references and online tools you used.


...
