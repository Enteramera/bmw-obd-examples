import customtkinter as ctk
import obd
import threading
import time

class OBDDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("OBD-II Live Dashboard")
        self.geometry("600x400")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        # OBD Setup
        self.obd_connection = None
        self.running = False

        # GUI Setup
        self.status_var = ctk.StringVar(value="🔌 Not Connected")
        self.rpm_var = ctk.StringVar(value="RPM: ---")
        self.speed_var = ctk.StringVar(value="Speed: ---")
        self.temp_var = ctk.StringVar(value="Temp: ---")

        self.create_widgets()
        self.auto_connect()

    def create_widgets(self):
        ctk.CTkLabel(self, textvariable=self.status_var, font=ctk.CTkFont(size=15)).pack(pady=10)

        ctk.CTkLabel(self, textvariable=self.rpm_var, font=ctk.CTkFont(size=18)).pack(pady=10)
        ctk.CTkLabel(self, textvariable=self.speed_var, font=ctk.CTkFont(size=18)).pack(pady=10)
        ctk.CTkLabel(self, textvariable=self.temp_var, font=ctk.CTkFont(size=18)).pack(pady=10)

        self.toggle_btn = ctk.CTkButton(self, text="Start Dashboard", command=self.toggle_dashboard)
        self.toggle_btn.pack(pady=20)

    def auto_connect(self):
        try:
            ports = obd.scan_serial()
            if not ports:
                self.status_var.set("🔌 No OBD-II ports found")
                return
            self.obd_connection = obd.OBD(ports[0])  # Auto-connect to the first available port
            if self.obd_connection.is_connected():
                self.status_var.set("✅ Connected to OBD-II")
            else:
                self.status_var.set("❌ Failed to connect")
        except Exception as e:
            self.status_var.set(f"❌ Error: {str(e).upper()}")

    def toggle_dashboard(self):
        if self.running:
            self.running = False
            self.toggle_btn.configure(text="Start Dashboard")
        else:
            if self.obd_connection and self.obd_connection.is_connected():
                self.running = True
                self.toggle_btn.configure(text="Stop Dashboard")
                threading.Thread(target=self.update_loop, daemon=True).start()
            else:
                self.status_var.set("⚠️ Not connected to OBD")

    def update_loop(self):
        while self.running:
            rpm_resp = self.obd_connection.query(obd.commands.RPM)
            speed_resp = self.obd_connection.query(obd.commands.SPEED)
            temp_resp = self.obd_connection.query(obd.commands.COOLANT_TEMP)

            rpm = rpm_resp.value.magnitude if rpm_resp.value else "---"
            speed = speed_resp.value.to("km/h").magnitude if speed_resp.value else "---"
            temp = temp_resp.value.to("degC").magnitude if temp_resp.value else "---"

            self.rpm_var.set(f"🌀 RPM: {rpm}")
            self.speed_var.set(f"🚗 Speed: {speed} km/h")
            self.temp_var.set(f"🌡️ Temp: {temp} °C")

            time.sleep(1)

if __name__ == "__main__":
    app = OBDDashboard()
    app.mainloop()