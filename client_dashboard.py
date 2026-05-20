import streamlit as st
import datetime
import socket
import json

st.title("Client Log Entry Dashboard")

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9090

# Log Level
level = st.selectbox(
    "Log Level",
    ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
)

# Service Categories
service_categories = {
    "Core Services": [
        "auth-service",
        "user-service",
        "api-gateway"
    ],

    "Business Services": [
        "payment-service",
        "order-service",
        "inventory-service"
    ],

    "Infrastructure Services": [
        "database-service",
        "logging-service",
        "analytics-service"
    ]
}

category = st.selectbox("Service Category", list(service_categories.keys()))

service = st.selectbox("Service", service_categories[category])

component = st.text_input("Component / Module")

message = st.text_area("Log Message")

# Submit Button
if st.button("Submit Log"):

    try:

        log_data = {
            "timestamp": str(datetime.datetime.now()),
            "client_ip": socket.gethostbyname(socket.gethostname()),
            "level": level,
            "category": category,
            "service": service,
            "component": component,
            "message": message
        }

        # Convert to JSON string
        log_json = json.dumps(log_data)

        # Create socket connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((SERVER_HOST, SERVER_PORT))

        # Send data
        s.sendall(log_json.encode())

        s.close()

        st.success("Log sent to server successfully!")

    except Exception as e:
        st.error(f"Connection failed: {e}")