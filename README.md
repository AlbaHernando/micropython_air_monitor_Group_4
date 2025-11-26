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

## 1. Project Overview
**Problem Statement**

Indoor Air Quality (IAQ) is a critical factor influencing human health, comfort, and productivity. Pollutants such as particulate matter (PM2.5/PM10), high levels of Carbon Dioxide (CO2), and volatile organic compounds (VOCs) can accumulate in poorly ventilated indoor environments like homes, schools, and offices. Many of these spaces lack real-time, accessible monitoring, leaving occupants unaware of potential health risks.

**Proposed Solution**

This project aims to design and build a cost-effective, real-time Indoor Air Quality monitoring system using an ESP32 FireBeetle microcontroller programmed in MicroPython.

The system will:

1.  **Measure key environmental parameters:**
    -   Temperature & Humidity
    -   General Air Quality (CO2 proxy, VOCs)
    -   Particulate Matter (PM2.5 & PM10)
2.  **Display the data locally** on an OLED screen for immediate feedback to occupants.
3.  **Transmit the collected data via Wi-Fi** to a cloud-based web dashboard for remote monitoring and historical data logging.




## 2. Hardware Components

This section details the hardware selected for the prototype. The components are chosen to balance cost, ease of integration with MicroPython, and the ability to meet the project's monitoring requirements.

### Component Visual Overview

<table align="center">
  <tr>
    <td align="center" width="33%">
      <img src="https://github.com/user-attachments/assets/ae15a0fd-06b0-45d0-bb53-72c08e412a20" alt="ESP32 FireBeetle" width="95%">
      <br>
      <em>Main Controller (ESP32)</em>
    </td>
    <td align="center" width="33%">
      <img src="https://github.com/user-attachments/assets/e3ff0a67-f6a2-4fb7-a812-33316e15e527" alt="GP2Y10 Particules sensor" width="95%">
      <br>
      <em>GP2Y10 Particules sensor</em>
    </td>
    <td align="center" width="33%">
      <img src="https://github.com/user-attachments/assets/b87f8879-f5fa-497d-8490-917ca713a047" alt="DHT11 Temperature and Humidity sensor" width="95%">
      <br>
      <em>DHT11 Temperature and Humidity sensor</em>
    </td>
  </tr>
  
  <tr>
    <td align="center" width="33%">
      <img src="https://github.com/user-attachments/assets/158a1572-d56c-4f0d-95f1-2d5a76e697ce" alt="MQ-135 CO2 sensor" width="95%">
      <br>
      <em>MQ-135 CO2 sensor</em>
    </td>
    <td align="center" width="33%">
      <img src="https://github.com/user-attachments/assets/232918aa-34fe-408a-a5ac-71618d92a3c1" alt="1 3-I2C-OLED" width="95%">
      <br>
      <em>1 3-I2C-OLED</em>
    </td>
    <td align="center" width="33%">
      <img src="LINK" alt="Description image" width="95%">
      <br>
      <em>Descripción Imagen 6</em>
    </td>
  </tr>
</table>
<br>e>
<br> 


### Component List & Functions

| Component | Type | Primary Role / Function |
| :--- | :--- | :--- |
| **ESP32 FireBeetle** | MCU | Main controller; manages sensors, data processing, and Wi-Fi transmission to the cloud. |
| **DHT12 (or DHT22)** | Sensor | Measures ambient Temperature and Relative Humidity (digital output). |
| **MQ-135** | Sensor | Detects general air quality gases (VOCs, smoke) acting as a proxy for poor ventilation (analog output). |
| **SDS011** | Sensor | Uses laser scattering to precisely count fine dust particles (PM2.5 & PM10) (UART serial). |
| **OLED Display (0.96")**| Output | Provides immediate real-time visual feedback of readings to occupants (I2C). |
| **Status LEDs** | Output | Red/Yellow/Green traffic-light indicators for quick "at-a-glance" air quality status. |
| **Breadboard & Wires**| Prototyping | Solderless infrastructure for rapid circuit building and testing. |
  



## 3. Software description

We created a flowchart for each measurement (Temperature, Humidity, CO2 and Particles), and one final flowchard unifiying all the parameters, integrating the function of Wi-Fi and the monitoring of data, being this flowchard the main program. Each of the individual flowchards of the measurements will be a subclass in MicroPython.


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



## 4. Instructions and photos
Describe how to use the application. Add photos or videos of your application.

## 5. References and tools
Put here the references and online tools you used.


...
