import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import webview
import threading
import psutil
import datetime
import platform
from friday_core import run_friday  # renamed from main.py

class FridayAPI:
    def get_system_info(self):
        cpu = psutil.cpu_percent(interval=0.5)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent

        battery = psutil.sensors_battery()
        battery_percent = battery.percent if battery else None

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return {
            "cpu": cpu,
            "ram": ram,
            "disk": disk,
            "battery": battery_percent,
            "datetime": now,
            "os": platform.system(),
            "os_version": platform.release(),
            "processor": platform.processor()
        }

def start_friday_thread():
    friday_thread = threading.Thread(target=run_friday, daemon=True)
    friday_thread.start()

if __name__ == '__main__':
    start_friday_thread()

    api = FridayAPI()
    window = webview.create_window("FRIDAY AI", "index.html", width=1000, height=700, js_api=api)
    webview.start()