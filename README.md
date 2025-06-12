# 🖥️ Multiseat Manager GUI for Linux

A modern graphical interface for easily configuring and managing multiseat setups on Linux systems. Designed to simplify the process of assigning users, devices, and displays to multiple seats — without needing to use `loginctl` or write complex `udev` rules manually.

---

## 🎯 Purpose

Multiseat setups allow multiple users to share a single Linux system, each with their own monitor, keyboard, and mouse. This project provides a user-friendly GUI for:

- Viewing connected input/output devices
- Creating, updating, and removing seats
- Assigning or detaching devices from specific seats

---


## 🧱 Tech Stack

- **Python 3.13**
- **PyQt5** – for building the GUI
- `loginctl`, `udevadm` – for interacting with systemd and udev
- `subprocess` – for shell command execution

---
## 📁 Project Structure & Architecture 
This project uses Clean Architecture, organizing code into four main layers:
- Domain: Core entities like Seat and Device, pure logic with no dependencies.
- Use Cases: Application logic — actions like assigning devices to seats.
- Interface Adapters: Bridges between GUI/system and core logic — includes controllers and gateways.
- Frameworks: Outer layer — PyQt5 GUI, system tools (loginctl, udevadm).


## 🚀 Installation
(To be added)
