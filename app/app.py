from flask import Flask, jsonify
import os
import socket
from datetime import datetime

app = Flask(__name__)

# Environment variables
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
PLATFORM_TEAM = os.getenv("PLATFORM_TEAM", "platform-engineering")
VERSION = os.getenv("VERSION", "v1")

# Sample employee data
employees = [
    {
        "employee_id": 101,
        "employee_name": "Navathej Annam",
        "department": "DevOps"
    },
    {
        "employee_id": 102,
        "employee_name": "Anjali Verma",
        "department": "Platform Engineering"
    },
    {
        "employee_id": 103,
        "employee_name": "Kiran Kumar",
        "department": "Cloud Operations"
    }
]

# Root Endpoint
@app.route("/")
def home():
    return jsonify({
        "application": "Employee Management API",
        "environment": ENVIRONMENT,
        "message": "Application is running successfully",
        "hostname": socket.gethostname()
    })

# Employee Endpoint
@app.route("/employees")
def get_employees():
    return jsonify({
        "employees": employees
    })

# Health Endpoint
@app.route("/health")
def health():
    return jsonify({
        "status": "UP"
    }), 200

# Information Endpoint
@app.route("/info")
def info():
    return jsonify({
        "environment_name": ENVIRONMENT,
        "platform_team": PLATFORM_TEAM,
        "version": VERSION,
        "deployment_time": str(datetime.now()),
        "hostname": socket.gethostname()
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)