## Indoor air quality monitoring system

* [1. Project Overview](#1-project-overview)
* [2. Hardware Components](#2-hardware-components)
* [3. Software description](#3-software-description)
* [4. Instructions and photos](#4-instructions-and-photos)
* [5. References and tools](#5-references-and-tools)

## Project 1: ESP32 Indoor Air Quality Monitor
Course: BPA-DE2 (Digital Electronics) 2025/26 Team Members:

- Xabier Asla    (responsible for ...)

- Alba Hernando  (responsible for ...)

- Pablo Vicente  (responsible for ...)


## 1. Project Overview
**Problem Statement**

Indoor Air Quality (IAQ) is a critical factor influencing human health, comfort, and productivity. Pollutants such as particulate matter (PM2.5/PM10), high levels of Carbon Dioxide (CO2), and volatile organic compounds (VOCs) can accumulate in poorly ventilated indoor environments like homes, schools, and offices. Many of these spaces lack real-time, accessible monitoring, leaving occupants unaware of potential health risks.

**Proposed Solution**

This project aims to design and build a cost-effective, real-time Indoor Air Quality monitoring system using an ESP32 FireBeetle microcontroller programmed in MicroPython.

The system will:

Measure key environmental parameters:

- Temperature & Humidity

- General Air Quality (CO2, VOCs)

- Particulate Matter (PM2.5 & PM10)

- Display the data locally on an OLED screen for immediate feedback.

- Transmit the collected data via Wi-Fi to a cloud-based web dashboard for remote monitoring and historical data logging.

## 2. Hardware Components

The following components have been selected to build the prototype.

- MCU (Microcontroller): ESP32
- Air quality / CO2: A MQ-135 sensor
- Temperature and Humidity: A DHT12 sensor
- Resistors
- LEDS
- Wires

  _WHY??????_
  

<p align="center">
  <img alt="DHT22 Sensor" src="https://github.com/user-attachments/assets/868c60fd-8720-4029-99f0-47ca6c41ce31" width="200">
  <br>
  <em>ESP32 Microcontroller</em>
</p>
<p align="center">
  <img alt="DHT22 Sensor" src="https://github.com/user-attachments/assets/158a1572-d56c-4f0d-95f1-2d5a76e697ce" width="200">
  <br>
  <em>MQ-135 Quality Air sensor</em>
</p>

<p align="center">
  <img alt="DHT22 Sensor" src="https://github.com/user-attachments/assets/b87f8879-f5fa-497d-8490-917ca713a047" width="200">
  <br>
  <em>DHT11 Temperature and Humidity sensor</em>
</p>

<p align="center">
  <img alt="DHT22 Sensor" src="https://github.com/user-attachments/assets/e3ff0a67-f6a2-4fb7-a812-33316e15e527" width="200">
  <br>
  <em>GP2Y10 Particules sensor</em>
</p>

<table align="center">
  <tr>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/158a1572-d56c-4f0d-95f1-2d5a76e697ce" alt="MQ-135 CO2 sensor" width="200">
      <br>
      <em>MQ-135 Quality Air sensor</em>
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/b87f8879-f5fa-497d-8490-917ca713a047" alt="DHT11 Temperature and Humidity sensor" width="200">
      <br>
      <em>DHT12 Temperature and Humidity sensor</em>
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/e3ff0a67-f6a2-4fb7-a812-33316e15e527" alt="GP2Y10 Particules sensorr" width="200">
      <br>
      <em>GP2Y10 Particules sensor</em>
    </td>
  </tr>
</table>





## 3. Software description

We created a flowchart for each measurement (Temperature-Humidity, CO2 and Particles), and one final flowchard unifiying all the parameters, integrating the function of Wi-Fi and the monitoring of data, being this flowchard the main program. Each of the individual flowchards of the measurements will be a subclass in MicroPython.


### DHT22 Sensor Logic (Temperature & Humidity)

A unified flowchart has been developed for the DHT22 sensor. Since this single hardware component measures both temperature and humidity, combining their logic accurately reflects the sequential reading and processing workflow, optimizing code structure and display output.

<details>
  <summary>▶️ <strong>Click here to expand the Flowchart of sensor DHT12 (Temperature & Humidity)</strong></summary>
  <br>
  <p align="center">
    <img src="https://github.com/user-attachments/assets/71356aa2-b297-4aa2-b404-84ab8e8e66e4" alt="DHT12 Combined Flowchart" width="800">
    <br>
    <em>Logic for Temperature and Humidity Sequential Processing</em>
  </p>
</details>











## 4. Instructions and photos
Describe how to use the application. Add photos or videos of your application.

## 5. References and tools
Put here the references and online tools you used.


...
