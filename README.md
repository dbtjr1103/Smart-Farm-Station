# Basil Cultivation Smart Farm Station

## Introduction

This project aims to develop a smart farm system for basil cultivation. It utilizes an AI-based monitoring system and automated environmental control to achieve efficient plant cultivation.

## Technology Stack & Tools

- **Programming Language**: Python
- **Web Framework**: Streamlit
- **AI Modeling**: YOLOv8 for image detection
- **Hardware Control**: W5100S-EVB-Pico board, TCP communication for smart farm control
- * ![image](https://github.com/dbtjr1103/Smart-Farm-Station/assets/115054808/56431b6c-4353-4976-a8ac-751a3e7a7263)

## Team Composition & Roles

- **My Role**:
  - AI Modeling: Using YOLOv8 for analyzing plant growth and health status

  - Web Application Development: Building an interface with Streamlit
  - * ![image](https://github.com/dbtjr1103/Smart-Farm-Web-Controller/assets/115054808/48c0975e-cfea-4f37-a1c8-d1f3999d27e2)
      
  - Camera Server Setup: Capturing and transmitting real-time images from the smart farm
  - * ![image](https://github.com/dbtjr1103/Smart-Farm-Station/assets/115054808/a43a83cf-769f-4c9a-b1c8-e42dedbac6e1)


- **Theo's Role**:
  - Smart Farm Control System Development: Managing hardware and sensor data integration for the smart farm
  - ![ezgif com-video-to-gif (1)](https://github.com/dbtjr1103/Smart-Farm-Station/assets/115054808/7a7f6e59-6371-4bf9-8dc2-a83a2dd9125c)

## Web Application Design & Features

1. **Real-Time Monitoring**
   - The web application, developed using Streamlit, enables users to view real-time images and sensor data (temperature, humidity, brightness) of the smart farm.
   - Supports database reset functionality.
   - ![Real-Time Monitoring Image](https://github.com/dbtjr1103/Smart-Farm-Station/assets/115054808/5ab784d6-cebe-4dfe-8953-bd2ab7ad7d09)

2. **Start Cultivation Button**
   - Pressing the 'Start Cultivation' button sends optimal initial values for basil cultivation (Temperature: 23°C, Humidity: 55%, Brightness: 500, Watering Cycle: 36 hours) to the TCP Client controlling the sensors via the Pico.
   - Initiates the display of growth information (e.g., time elapsed since cultivation start, current growth stage).
   - ![Start Cultivation Button](https://github.com/dbtjr1103/Smart-Farm-Station/assets/115054808/a105bbc8-6f9d-4125-b0b4-fb4b2be417b3)

3. **Current Status Button**
   - The 'Current Status' button fetches and displays the latest image from the Camera server, updating the on-screen visuals with the current status of the smart farm.
   - ![image](https://github.com/dbtjr1103/Smart-Farm-Station/assets/115054808/cdf8840e-5992-460d-8ef7-4a01a680e5ef)



## Results & Future Plans

As of the current date (November 28, 2023), the smart farm system has been set up, and basil has been planted. It is expected that cotyledons (seed leaves) will develop around 7 to 10 days after planting. Updates will be provided as the plants grow and reach different stages of development. Stay tuned for further updates on the progress and growth of the basil in our smart farm system.
- ![image](https://github.com/dbtjr1103/Smart-Farm-Station/assets/115054808/2db0a070-7173-47aa-b0c6-8e7e3dca9f2b)

