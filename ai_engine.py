import socket
import csv
import os
import threading
from datetime import datetime

HOST = "127.0.0.1"
PORT = 9091
LOG_FILE = "logs.csv"

lock = threading.Lock()

def write_log(client_ip, level, category, service, component, message):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_exists = os.path.isfile(LOG_FILE)

    with lock:
        with open(LOG_FILE, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow(["timestamp", "client_ip", "level", "category", "service", "component", "message"])

            writer.writerow([timestamp, client_ip, level, category, service, component, message])


def handle_connection(conn):

    data = conn.recv(1024).decode()

    if data:
        try:
            client_ip, level, category, service, component, message = data.split("|", 5)
            write_log(client_ip.strip(), level.strip(), category.strip(), service.strip(), component.strip(), message.strip())
            print("Stored:", data)
        except Exception as e:
            print("Invalid format:", data)

    conn.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(10)

print("AI Engine running (multi-client)...")

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_connection, args=(conn,))
    thread.start()