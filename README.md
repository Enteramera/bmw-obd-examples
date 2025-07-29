# BMW OBD Examples 🚗🔧

This repository contains simple Python examples for communicating with an OBD-II adapter using the [`python-OBD`](https://github.com/brendan-w/python-OBD) library.  
The graphical user interfaces are built using [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter).

---

## 📁 Project Structure

```plaintext
obd-examples/
├── connection_gui.py         # GUI for manually connecting/disconnecting to OBD-II
├── live_dashboard.py         # Real-time dashboard (RPM, speed, temperature)
├── voltage_reader.py         # Live battery voltage display using a custom command
```

## ▶️ Voraussetzungen
- Python 3.10+
- OBD-II Bluetooth or USB adapter
- Car with an active OBD-II port
---
## 📦 Installation

```bash
pip install python-OBD customtkinter
