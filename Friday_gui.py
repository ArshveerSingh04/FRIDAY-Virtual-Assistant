import tkinter as tk
import math
import psutil
import datetime
import random

class FridayUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FRIDAY AI")
        self.root.config(bg="black")

        # Canvas for central animation
        self.canvas = tk.Canvas(root, width=600, height=600, bg="black", highlightthickness=0)
        self.canvas.pack(side="left")

        # Right panel for system info
        self.info_frame = tk.Frame(root, bg="black")
        self.info_frame.pack(side="right", fill="y", padx=10)

        self.sys_label = tk.Label(self.info_frame, text="", font=("Consolas", 12), fg="red", bg="black", justify="left")
        self.sys_label.pack(anchor="n")

        self.angle = 0
        self.animate()
        self.update_system_stats()

    def animate(self):
        """Create FRIDAY's animated face"""
        self.canvas.delete("all")

        # Central core (glowing orb)
        self.canvas.create_oval(250, 250, 350, 350, fill="#FF1C1C", outline="red", width=3)

        # Rotating rings (particles)
        for i in range(10):
            radius = 100 + i*15
            x = 300 + radius * math.cos(self.angle + i)
            y = 300 + radius * math.sin(self.angle + i)
            self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="red")

        self.angle += 0.05
        self.root.after(50, self.animate)

    def update_system_stats(self):
        """Update system info panel"""
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        battery = psutil.sensors_battery()
        temp = random.randint(45, 75)  # placeholder temperature

        time_now = datetime.datetime.now().strftime("%H:%M:%S  %d-%m-%Y")

        stats = f"""
FRIDAY AI SYSTEM MONITOR
-------------------------
🖥️ CPU Usage     : {cpu}%
💾 RAM Usage     : {ram}%
📀 Disk Usage    : {disk}%
🌡️ Temp (CPU)   : {temp}°C
🔋 Battery       : {battery.percent if battery else 'N/A'}%
⏰ Time & Date   : {time_now}
"""
        self.sys_label.config(text=stats)
        self.root.after(1000, self.update_system_stats)

# Run the FRIDAY UI
if __name__ == "__main__":
    root = tk.Tk()
    ui = FridayUI(root)
    root.mainloop()
