# BMW OBD Examples 🚗🔧

Dieses Repository enthält einfache Python-Beispiele zur Kommunikation mit einem OBD-II Adapter über die [`python-OBD`](https://github.com/brendan-w/python-OBD) Bibliothek.  
Die grafischen Oberflächen sind mit [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) umgesetzt.

---

## 📁 Projektstruktur

```plaintext
obd-examples/
├── connection_gui.py         # GUI zum manuellen Verbinden/Trennen von OBD-II
├── live_dashboard.py         # Echtzeit-Dashboard (RPM, Speed, Temperatur)
├── voltage_reader.py         # Live-Anzeige der Batteriespannung über Custom Command
```

## ▶️ Voraussetzungen
- Python 3.10+
- OBD-II Bluetooth/USB-Adapter
- Auto mit aktivem OBD-II Anschluss
---
## 📦 Installation

```bash
pip install python-OBD customtkinter
