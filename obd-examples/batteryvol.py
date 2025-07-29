import customtkinter as ctk
import obd
import threading
import time
from obd import OBDCommand, Unit
from obd.protocols import ECU
"""
    --> obd.commands.CONTROL_MODULE_VOLTAGE
    This command retrieves the voltage of the battery or control module.
    R* = A * 256 + B / 100     | R* = Result in Volts
"""
class CONTROL_MODULE_VOLTAGE(OBDCommand):
    def __init__(self):
        name = "Control_Module_Voltage"
        desc = "Control Module Voltage (Battery)"
        command = "01 42" # Custom Command (https://python-obd.readthedocs.io/en/latest/Custom%20Commands/)
        bytes_returned = 2
        unit = Unit.VOLT
        ecu = ECU.ENGINE
        fast = True

        def voltage_decoder(msgs):
            data = msgs[0].data # raw hex bytes into 
            A = int(data[2], 16) # first byte
            B = int(data[3], 16) # second byte
            voltage = (A * 256 + B) / 100.0 # convert to volts
            return voltage
        
        super().__init__(
            name=name,
            desc=desc,
            command=command,
            bytes_returned=bytes_returned,
            decoder=voltage_decoder,
            ECU=ecu,
            fast=fast,
            unit=unit
        )

class OBDDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("OBD-II Live Dashboard")
        self.geometry("500x400")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.obd_connection = None
        self.running = False

        # GUI vars
        self.status_var = ctk.StringVar(value="Not Connected")
        self.voltage_var = ctk.StringVar(value="Voltage: ---")

        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, textvariable=self.status_var, font=ctk.CTkFont(size=15)).pack(pady=10)

        ctk.CTkLabel(self, textvariable=self.voltage_var, font=ctk.CTkFont(size=22)).pack(pady=20)

        self.toggle_btn = ctk.CTkButton(self, text="Start Voltage Monitor", command=self.toggle_dashboard)
        self.toggle_btn.pack(pady=20)

    def toggle_dashboard(self):
        if self.running:
            self.running = False
            self.toggle_btn.configure(text="Start Voltage Monitor")
        else:
            try:
                if self.obd_connection is None or not self.obd_connection.is_connected():
                    ports = obd.scan_serial()
                    if not ports:
                        self.status_var.set("No OBD-II ports found")
                        return
                    self.obd_connection = obd.OBD(ports[0])
                if self.obd_connection.is_connected():
                    self.running = True
                    self.toggle_btn.configure(text="Stop Voltage Monitor")
                    self.status_var.set("Connected – Reading Voltage")
                    threading.Thread(target=self.update_loop, daemon=True).start()
                else:
                    self.status_var.set("Failed to connect to OBD-II")
            except Exception as e:
                print("Failed to start:", e)
                self.status_var.set("Connection error")

    def update_loop(self):
        cmd = CONTROL_MODULE_VOLTAGE()
        while self.running:
            response = self.obd_connection.query(cmd)
            if response and response.value is not None:
                voltage = round(response.value, 2)
                self.voltage_var.set(f"Voltage: {voltage} V")
            else:
                self.voltage_var.set("Voltage: ---")
            time.sleep(1)


if __name__ == "__main__":
    app = OBDDashboard()
    app.mainloop()