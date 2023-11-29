import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh
import socket
import threading
import time
import random
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import os
from glob import glob

# TCP 서버 설정
HOST = '192.168.0.2'  # 서버의 IP 주소
PORT = 5001           # 서버의 포트 번호

# 서버와 클라이언트 관리를 위한 변수
server = None
clients = []
server_running = False

# DB 생성 및 연결
def create_connection():
    conn = sqlite3.connect('sensor_data.db')
    return conn

# 테이블 생성
def create_table(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sensor_data
                 (date text, temperature real, humidity real, brightness integer)''')
    conn.commit()

# DB에 데이터 저장
def save_data_to_db(temp, humi, bright):
    with create_connection() as conn:
        c = conn.cursor()
        # adc_result를 밝기로 사용
        c.execute("INSERT INTO sensor_data (date, temperature, humidity, brightness) VALUES (?, ?, ?, ?)",
                  (datetime.now(), temp, humi, bright))
        conn.commit()


def send_data(conn):
    while True:
        # 최적의 데이터 생성
        temp = 23 # 고정된 온도 값
        humi = 55 # 고정된 습도 값
        bright = 500  # 고정된 밝기 값

        # 데이터 문자열로 포맷팅
        data = f"{temp}.{humi}.{bright}.1\n"

        try:
            # 데이터 송신
            conn.sendall(data.encode())
        except:
            break

        # 5초 대기
        time.sleep(5)
        
# TCP 클라이언트로부터 데이터를 보내는 함수
def send_custom_data(client_socket, data):
    try:
        client_socket.sendall(data.encode())
        print("데이터 송신 완료:", data)
    except Exception as e:
        print("데이터 송신 오류:", e)

def tcp_client_send_data():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('192.168.0.11', 5000))
        print("TCP 클라이언트가 서버에 연결되었습니다.")
        
        time.sleep(5)
        # '재배 시작' 버튼을 눌렀을 때 전송할 데이터
        data_to_send = "23.55.500.1"
        send_custom_data(client_socket, data_to_send)
        
        # 필요한 추가 로직을 여기에 구현...

    except Exception as e:
        print("TCP 클라이언트 연결 오류:", e)
    finally:
        client_socket.close()
        
def client_thread(conn, addr):
    print(f"[연결됨] {addr} 연결됨.")

    # 랜덤 데이터 전송을 위한 스레드 시작
    threading.Thread(target=send_data, args=(conn,)).start()

    while True:
        try:
            # 클라이언트로부터 데이터 수신
            received_data = conn.recv(1024).decode()
            if not received_data:
                break
            print(f"[수신된 데이터] {addr}: {received_data}")

            # 수신된 데이터 파싱
            data_parts = received_data.split(', ')
            temp = float(data_parts[0].split(' : ')[1])
            humi = float(data_parts[1].split(' : ')[1])
            bright = int(data_parts[2].split(' : ')[1])

            # 데이터베이스에 저장
            save_data_to_db(temp, humi, bright)
        except:
            break

    conn.close()
    print(f"[연결해제] {addr} 연결해제.")

# 데이터베이스 연결 및 테이블 생성
db_conn = create_connection()
create_table(db_conn)

def plot_sensor_data(data):
    # 새로운 figure 및 축 생성
    fig, axs = plt.subplots(3, 1, figsize=(12, 6))

    # 날짜, 온도, 습도, 밝기 데이터 추출
    dates = [datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f') for row in data]
    temperatures = [row[1] for row in data]
    humidities = [row[2] for row in data]
    brightnesses = [row[3] for row in data]

    # 첫 번째 축에 온도 그래프 그리기
    axs[0].plot(dates, temperatures, label='Temperature', color='red')
    axs[0].set_ylabel('Temperature (℃)')
    axs[0].legend(loc='upper left')

    # 두 번째 축에 습도 그래프 그리기
    axs[1].plot(dates, humidities, label='Humidity', color='blue')
    axs[1].set_ylabel('Humidity (%)')
    axs[1].legend(loc='upper left')

    # 세 번째 축에 밝기 그래프 그리기
    axs[2].plot(dates, brightnesses, label='Brightness', color='green')
    axs[2].set_ylabel('Brightness')
    axs[2].legend(loc='upper left')

    # 레이아웃 조정
    plt.tight_layout()

    # Streamlit에 그래프 표시
    st.pyplot(fig)

    # 그래프 닫기
    plt.close(fig)

def get_sensor_data(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM sensor_data ORDER BY date DESC LIMIT 100")
    data = c.fetchall()
    return data

# def display_graph():
#     with create_connection() as conn:
#         sensor_data = get_sensor_data(conn)
#     plot_sensor_data(sensor_data)  # 데이터 전달

def display_table():
    with create_connection() as conn:
        sensor_data = get_sensor_data(conn)
    # 데이터를 pandas DataFrame으로 변환
    df = pd.DataFrame(sensor_data, columns=['Date', 'Temperature', 'Humidity', 'Brightness'])
    st.table(df)  # 스트림릿 테이블로 표시

def start_server():
    global server, server_running
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    server_running = True
    print(f"[시작] 서버가 {HOST}:{PORT}에서 시작됨.")

    while server_running:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=client_thread, args=(conn, addr))
        thread.start()

def stop_server():
    global server, server_running
    if server:
        server_running = False
        for conn in clients:
            conn.close()
        server.close()
        print("[종료] 서버 종료됨.")
        
def tcp_client_connect():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('192.168.0.11', 5000))
        print("TCP 클라이언트가 서버에 연결되었습니다.")

        # 데이터 버퍼 초기화
        data_buffer = ''

        while True:
            # 서버로부터 데이터 수신
            data = client_socket.recv(1024).decode()
            if not data:
                break

            # 데이터 버퍼에 추가
            data_buffer += data

            # 줄바꿈 기준으로 데이터 분리
            while '\n' in data_buffer:
                line, data_buffer = data_buffer.split('\n', 1)
                # 데이터 파싱
                try:
                    data_parts = line.split(', ')
                    temp = float(data_parts[0].split(' : ')[1])
                    humi = float(data_parts[1].split(' : ')[1])
                    bright = int(data_parts[2].split(' : ')[1])
                    # 데이터베이스에 저장
                    save_data_to_db(temp, humi, bright)
                except ValueError as e:
                    print("데이터 파싱 오류:", e)

            # 1초 대기
            time.sleep(1)

    except Exception as e:
        print("TCP 클라이언트 연결 오류:", e)
    finally:
        client_socket.close()
        
# DB 초기화 함수
def reset_database():
    with create_connection() as conn:
        c = conn.cursor()
        # 기존 테이블 삭제
        c.execute("DROP TABLE IF EXISTS sensor_data")
        # 테이블 다시 생성
        create_table(conn)
        st.success("데이터베이스가 초기화되었습니다.")

# 페이지 자동 새로고침 설정 (예: 1초마다)
st_autorefresh(interval=5000, key="data_refresh")

# 상단 제목
st.title("🌱 Smart Farm")

# 이미지 파일 저장 경로
image_save_path = 'image'  # 현재 폴더 내에 'image' 폴더 사용
os.makedirs(image_save_path, exist_ok=True)  # 'image' 폴더가 없다면 생성

# 이미지 섹션
left_column, right_column = st.columns([2, 2])
with left_column:
    # '현재 상태' 버튼이 눌렸을 때, 이미지 다운로드 및 저장
    if 'refresh_image' in st.session_state:
        img_url = "http://192.168.0.10/16"
        response = requests.get(img_url)
        new_image_path = os.path.join(image_save_path, f'image_{st.session_state["refresh_image"].strftime("%Y%m%d%H%M%S")}.jpg')
        with open(new_image_path, 'wb') as file:
            file.write(response.content)
        st.session_state.pop('refresh_image')

    # 가장 최신의 이미지 파일 찾기
    list_of_files = glob(os.path.join(image_save_path, '*.jpg'))  # JPG 파일만 찾음
    if list_of_files:
        latest_image = max(list_of_files, key=os.path.getctime)
        img = Image.open(latest_image)
        st.image(img, use_column_width=True)
    else:
        st.write("저장된 이미지가 없습니다.")

st.markdown("""
    <style>
    /* 버튼의 크기 조정 */
    .st-emotion-cache-cfxelm.ef3psqc12 {
        font-size: 0.1em; /* 글씨체 크기 조정 */
        padding: 5px 10px; /* 내부 여백 조정 */
    }
    </style>
""", unsafe_allow_html=True)

# 버튼 섹션
button_columns = st.columns(5)
with button_columns[0]:
    if st.button('📸 현재 상태', key='current_status_button'):
        st.session_state['refresh_image'] = datetime.now()

# 버튼 섹션에서 재배 시작! 버튼에 함수 연결
with button_columns[1]:
    if st.button('🌱 재배 시작!', key='start_growing_button'):
        st.session_state['start_time'] = datetime.now()
        tcp_client_send_data()  # TCP 클라이언트로 데이터 전송

with button_columns[2]:
    if st.button('🔄 DB 초기화', key='reset_db_button'):
        reset_database()

with button_columns[3]:
    if st.button("🖥️ TCP Server", key='start_server_button'):
        if not server_running:
            server_thread = threading.Thread(target=start_server)
            server_thread.start()
            st.success("TCP 서버가 시작되었습니다.")
        else:
            st.error("TCP 서버가 이미 실행 중입니다.")


with button_columns[4]:
    if st.button('🔗 TCP Client', key='tcp_client_connect_button'):
        tcp_client_thread = threading.Thread(target=tcp_client_connect)
        tcp_client_thread.start()
        st.success("TCP 클라이언트가 연결되었습니다.")
        
# 슬라이더 섹션
with right_column:

    st.markdown("""
        <style>
        .optimal-conditions {
            text-align: left;
            font-size: small;
            color: #4CAF50;
            background-color: #E8F5E9;
            padding: 5px;
            border-radius: 5px;
            border: 2px solid #4CAF50;
            margin: 10px 0;
        }
        .optimal-conditions strong {
            color: #388E3C;
            font-size: large;
        }
        </style>
        <div class="optimal-conditions">
            <strong>바질 재배 최적의 조건</strong><br>
            - 🌊 급수주기: 주 1~2회<br>
            - 🌡️ 온도: 20~25°C (℃)<br>
            - 💧 습도: 40-70% (RH)<br>
            - ☀️ 밝기: 300 이상 (μmol/m²/s)
        </div>
    """, unsafe_allow_html=True)
        
    with create_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM sensor_data ORDER BY date DESC LIMIT 100")
        data = c.fetchall()
    
    # 날짜 형식을 'YYYY-MM-DD HH:MM'으로 변경
    formatted_data = []
    for row in data:
        formatted_date = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d %H:%M')
        formatted_data.append((formatted_date, row[1], row[2], row[3]))
    
    df = pd.DataFrame(formatted_data, columns=['날짜와 시간', '온도', '습도', '밝기'])
    st.dataframe(df)


# 하단 섹션 - 시간, 진행률, 성장 정보
with st.container():
    test_mode_multiplier = 100000
    total_days_for_harvest = 50
    current_time = datetime.now()

    if 'start_time' in st.session_state:
        test_elapsed_time = (current_time - st.session_state['start_time']) * test_mode_multiplier
    else:
        test_elapsed_time = timedelta()

    test_elapsed_days = test_elapsed_time / timedelta(days=1)
    progress_percentage = min((test_elapsed_days / total_days_for_harvest), 1.0)

    st.subheader('🌿 성장 정보')
    elapsed_hours = int(test_elapsed_time.total_seconds() / 3600)
    st.text(f"재배한 지 {int(test_elapsed_days)}일 {elapsed_hours % 24}시간이 지났어요.")

    if test_elapsed_days < 10:
        growth_stage = "발아 단계"
        stage_emoji = "🌱"
        stage_color = "brown"
    elif test_elapsed_days < 30:
        growth_stage = "성장 단계"
        stage_emoji = "🌿"
        stage_color = "green"
    elif test_elapsed_days < 50:
        growth_stage = "개화 단계"
        stage_emoji = "🌼"
        stage_color = "blue"
    else:
        growth_stage = "수확 단계"
        stage_emoji = "🍅"
        stage_color = "red"

    st.markdown(f"<span style='color: {stage_color};'>현재 {growth_stage} {stage_emoji}입니다.</span>", unsafe_allow_html=True)

    st.progress(progress_percentage)


                                                                                                                                                                   