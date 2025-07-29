import obd
import customtkinter as ctk


class OBDManager:
    def __init__(self):
        self.connection = None
        self.available_ports = obd.scan_serial()  # Scan for available OBD-II ports
        self.port = None

    def list_ports(self):
        return self.available_ports

    def connect(self, port=None, fast=True):
        if port:
            self.port = port
        else:
            self.port = self.available_ports[0] if self.available_ports else None

        if not self.port:
            return "NO OBD port found"

        try:
            self.connection = obd.OBD(self.port, fast=fast)
            if self.connection.is_connected():
                return f"Connected to {self.port}"
            else:
                return "Failed to connect to OBD-II port"
        except Exception as e:
            return f"Error connecting to OBD-II port: {str(e).upper()}"

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            return "Disconnected from OBD-II port"
        return "No active connection to disconnect, lol"

    def is_connected(self):
        return self.connection is not None and self.connection.is_connected()

    def get_connection(self):
        return self.connection


class OBDApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("OBD-II Connection")
        self.geometry("400x200")

        self.manager = OBDManager()
        self.port_var = ctk.StringVar()
        self.status_var = ctk.StringVar(value="Disconnected")

        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text="Available OBD-II Ports:", font=ctk.CTkFont(size=14)).pack(pady=10)

        ports = self.manager.list_ports()
        self.port_menu = ctk.CTkComboBox(self, values=ports, variable=self.port_var, state="readonly")

        if ports:
            self.port_menu.set(ports[0])
        self.port_menu.pack(pady=5)

        self.connect_btn = ctk.CTkButton(self, text="Connect", command=self.toggle_connection)
        self.connect_btn.pack(pady=15)

        self.status_label = ctk.CTkLabel(self, textvariable=self.status_var, font=ctk.CTkFont(size=12))
        self.status_label.pack(pady=10)

    def toggle_connection(self):
        if self.manager.is_connected():
            msg = self.manager.disconnect()
            self.connect_btn.configure(text="Connect")
        else:
            msg = self.manager.connect(port=self.port_var.get())
            if self.manager.is_connected():
                self.connect_btn.configure(text="Disconnect")

        self.status_var.set(msg)


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = OBDApp()
    app.mainloop()
