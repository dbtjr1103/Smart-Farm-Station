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
  -  ```python
     streamlit run main.py
     ```


- **Theo's Role**:
  - Smart Farm Control System Development: Managing hardware and sensor data integration for the smart farm
  - ![ezgif com-video-to-gif (1)](https://github.com/dbtjr1103/Smart-Farm-Station/assets/115054808/7a7f6e59-6371-4bf9-8dc2-a83a2dd9125c)

## Web Application Design & Features

1. **Real-Time Monitoring**
   - The web application, developed using Streamlit, enables users to view real-time images and sensor data (temperature, humidity, brightness) of the smart farm.
   - Supports database reset functionality.
   - ![Real-Time Monitoring Image](https://github.com/dbtjr1103/Smart-Farm-Station/assets/115054808/5ab784d6-cebe-4dfe-8953-bd2ab7ad7d09)
   - Code Example:
     ```python
     st.image(img, use_column_width=True)
     df = pd.DataFrame(sensor_data, columns=['Date', 'Temperature', 'Humidity', 'Brightness'])
     st.table(df)
     ```

2. **Start Cultivation Button**
   - Pressing the 'Start Cultivation' button sends optimal initial values for basil cultivation (Temperature: 23°C, Humidity: 55%, Brightness: 500, Watering Cycle: 36 hours) to the TCP Client controlling the sensors via the Pico.
   - Initiates the display of growth information (e.g., time elapsed since cultivation start, current growth stage).
   - ![Start Cultivation Button](https://github.com/dbtjr1103/Smart-Farm-Station/assets/115054808/a105bbc8-6f9d-4125-b0b4-fb4b2be417b3)
   - Code Example:
     ```python
     if st.button('🌱 재배 시작!', key='start_growing_button'):
         st.session_state['start_time'] = datetime.now()
         tcp_client_send_data()
     ```

3. **Current Status Button**
   - The 'Current Status' button fetches and displays the latest image from the Camera server, updating the on-screen visuals with the current status of the smart farm.
   - ![Current Status Image](https://github.com/dbtjr1103/Smart-Farm-Station/assets/115054808/cdf8840e-5992-460d-8ef7-4a01a680e5ef)
   - Code Example:
     ```python
     if 'refresh_image' in st.session_state:
         img_url = "http://192.168.0.10/16"
         response = requests.get(img_url)
         new_image_path = os.path.join(image_save_path, f'image_{st.session_state["refresh_image"].strftime("%Y%m%d%H%M%S")}.jpg')
         with open(new_image_path, 'wb') as file:
             file.write(response.content)
         st.session_state.pop('refresh_image')
     ```

## Results & Future Plans

As of the current date (November 28, 2023), the smart farm system has been set up, and basil has been planted. It is expected that cotyledons (seed leaves) will develop around 7 to 10 days after planting. Updates will be provided as the plants grow and reach different stages of development. Stay tuned for further updates on the progress and growth of the basil in our smart farm system.
- ![image](https://github.com/dbtjr1103/Smart-Farm-Station/assets/115054808/2db0a070-7173-47aa-b0c6-8e7e3dca9f2b)

Additionally, we plan to incorporate an AI model into the system. This AI feature will detect the condition of basil leaves, identifying whether they are healthy, affected by fusarium, or showing signs of powdery mildew. This enhancement aims to provide more precise and automated monitoring of plant health within the smart farm environment.
- ![image](https://github.com/dbtjr1103/Smart-Farm-Station/assets/115054808/3e65c70d-373f-49f8-9e62-d818c6d52053)
