## Indoor air quality monitoring system

* [1. Project Overview](#1-project-overview)
* [2. Hardware Components](#2-hardware-components)
* [3. Software description](#3-software-description)
* [4. Instructions and photos](#4-instructions-and-photos)
* [5. Project poster](#5-project-poster)
* [6. References and tools](#6-references-and-tools)

## Project 1: ESP32 Indoor Air Quality Monitor
Course: BPA-DE2 (Digital Electronics) 2025/26 Team 4, Members:

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

3.  **Visually Alert:** To make it obvious at a glance, it activates physical traffic-light LEDs corresponding to the global status.

4.  **Display Data Locally:** It shows the readings and status messages right on the OLED screen for immediate feedback to occupants.

5.  **Transmit Data:** Finally, it sends the logic collected data via Wi-Fi to a cloud-based dashboard for remote monitoring and historical logging.

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
  <img src="https://github.com/user-attachments/assets/76b5f611-0f84-4688-a067-f571cc7d533b" alt="Circuit Wiring Diagram" width="700">
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


The `main.py` script runs a continuous loop following the next steps in order:


1.  **Initialization:** When the system starts up, it first sets up all the hardware connections (the I2C bus, ADCs, and LEDs). We turn on the Green LED right away to show it has power. Then, it tries to connect to the Wi-Fi using the password we saved in `config.py`.


2.  **Measurement Cycle (Step 1):** The main script calls the functions we wrote for each sensor (like `analyze_T`, `analyze_H`, etc., which are in the `/lib` folder). Each function reads its own sensor hardware, checks if the value is okay based on our thresholds (determining if it's OK, Warning, or Danger), and sends back both the raw numbers and the status flags.


3.  **Global Status Determination (Step 2):** Once it has data from all sensors, the main script looks at all the status flags to decide the overall room status. We used a priority logic: **Red (Danger) is more important than Yellow (Warning), which is more important than Green (Ideal)**. It then turns on the correct physical LED on the breadboard.


4.  **Display Update (Step 3):** With the status LED on, the system goes through the sensor readings one by one and shows them on the OLED screen along with their status messages. We added a short pause between each one so it's easy to read.

5.  **Cloud Transmission (Step 4):** If the Wi-Fi connection is working, the system packs all the collected data and the global status into a payload and sends it to our cloud endpoint (ThingSpeak) using an HTTP POST request.
    * **ThingSpeak Channel Configuration:** We have set up a ThingSpeak channel with the following field mapping to store our data:
  
      
        | Field No. | Data Stored | Unit/Type |
        | :--- | :--- | :--- |
        | **Field 1** | Temperature | °C |
        | **Field 2** | Humidity | % |
        | **Field 3** | CO2 Proxy Value | Voltage |
        | **Field 4** | Particle Sensor Value | Voltage |
        | **Field 5** | Global System Status | String (e.g., "IDEAL") |
    * **Live Demo:** You can view the real-time data streaming to our public ThingSpeak dashboard here: **[https://api.thingspeak.com/update]**
    * *Note: The private `Write API Key` required for sending data is stored securely in the `config.py` file and is not exposed in this public documentation.*
    * *Note 2: We added a check so that if a sensor has a critical error, we skip sending data to maintain data integrity.*


6.  **Repeat:** Finally, it turns off the LEDs, waits a moment, and starts the whole cycle over again.




### 3.3 Software Flowcharts

Below are the flowcharts illustrating the logic for the main program and specific sensor sub-processes.

#### Main program

<details>
  <summary>▶️ <strong>Click here to expand the Flowchart of the main program</strong></summary>
  <br>
  <p align="center">
    <img src="https://github.com/user-attachments/assets/203762f3-a349-46bd-b811-794114ea5cb6" alt="Main program Flowchart" width="800">
    <br>
    <em>Logic for the main program</em>
  </p>
</details>


#### Temperature measurement and analysis logic

<details>
  <summary>▶️ <strong>Click here to expand the Flowchart of Temperature measurement and analysis logic </strong></summary>
  <br>
  <p align="center">
    <img src="https://github.com/user-attachments/assets/341e5e46-bee4-4cec-afc4-873229da5c38" alt="Temperature Flowchart" width="800">
    <br>
    <em>Logic for Temperature Processing</em>
  </p>
</details>


#### Humidity measurement and analysis logic

<details>
  <summary>▶️ <strong>Click here to expand the Flowchart of Humidity measurement and analysis logic </strong></summary>
  <br>
  <p align="center">
    <img src="https://github.com/user-attachments/assets/8073c73f-bedb-4156-a172-5377bd5d81f1" alt="Humidity Flowchart" width="800">
    <br>
    <em>Logic for Humidity Processing</em>
  </p>
</details>

#### CO2 proxy measurement and analysis logic

<details>
  <summary>▶️ <strong>Click here to expand the Flowchart of CO2 proxy measurement and analysis logic </strong></summary>
  <br>
  <p align="center">
    <img src="https://github.com/user-attachments/assets/86539a89-67cd-48f1-95b5-c50468441b13" alt="CO2 proxy Flowchart" width="800">
    <br>
    <em>Logic for CO2 proxy Processing</em>
  </p>
</details>


#### Particles measurement and analysis logic

<details>
  <summary>▶️ <strong>Click here to expand the Flowchart of Particles measurement and analysis logic </strong></summary>
  <br>
  <p align="center">
    <img src="https://github.com/user-attachments/assets/b0d33c72-ade7-4e57-bc18-94b95d0ac014" alt="Particles Flowchart" width="800">
    <br>
    <em>Logic for Particles Processing</em>
  </p>
</details>



---
## 4. Instructions and photos

### 4.1 Instructions

To be able to replicate and run this project you have to follow the next steps:

1.  **Hardware Assembly:** Assemble the circuit on a breadboard following the Wiring Diagram and Pinout Table provided in Section 2.3.


2.  **Firmware:** Ensure the ESP32 is flashed with MicroPython firmware.


3.  **File Upload:** Upload all files from this repository to the ESP32, maintaining the exact directory structure.


4.  **Configuration:** Edit the `config.py` file on the ESP32 to enter your local Wi-Fi SSID, Password, and your Cloud API Endpoint URL. **This step is crucial so that the microcontroller is able to connect to Wi-Fi and Cloud and it operates correctly. Make sure not to forget it.**


5.  **Execution:** Reset the ESP32. The `main.py` script should run automatically. The Green LED will light up initially, followed by Wi-Fi connection status on the OLED screen, and then the main measurement loop will begin.

### 4.2 Photographs and the video of the final project

<h2 align="center">Prototype Demonstration Video</h2>

<p align="center">
  <a href="https://www.youtube.com/watch?v=PON_AQUI_EL_ID_DE_TU_VIDEO_DE_YOUTUBE" target="_blank">
    <img src="https://img.youtube.com/vi/PON_AQUI_EL_ID_DE_TU_VIDEO_DE_YOUTUBE/maxresdefault.jpg" 
         alt="Watch the video demonstration" width="700" border="10" />
  </a>
  <br>
  <em>Video demonstration showing the functionality and operation of our Indoor Air Quality Monitor prototype.</em>
</p>

---

## 5. Project Poster

Below is the project poster summarizing the concept, design, and value proposition of the Indoor Air Quality Monitor.

<p align="center">
  <a href="PON_AQUI_EL_ENLACE_AL_ARCHIVO_DE_TU_POSTER_EN_GITHUB" target="_blank">
    <img src="PON_AQUI_EL_ENLACE_A_LA_IMAGEN_DE_TU_POSTER_EN_GITHUB" alt="Project Poster Thumbnail" width="800" style="border: 2px solid #ddd; border-radius: 4px; padding: 5px;">
  </a>
  <br>
  <em>Click on the image to view the full-size poster.</em>
</p>

---

## 6. References and Tools


* **Project Guide / Course Material:**
    * **Professor's GitHub Repository:** [GitHub](https://github.com/tomas-fryza/esp-micropython) - Used as a reference guide for project structure and code examples.
* **Documentation & Datasheets:**
    * **MicroPython Documentation:** https://docs.micropython.org/
    * **ESP32 Pinout Reference:** Espressif Systems documentation.
    * **Sensor Datasheets:** Used for timing and calibration (DHT12, MQ-135, GP2Y10).
* **Development Tools:**
    * **IDE:** Thonny IDE.
    * **Diagramming:** [Draw.io](https://www.drawio.com/) (used for flowcharts) and [EasyEDA](https://easyeda.com/es) (used for wiring diagrams).

---





...
