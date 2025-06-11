# 🖥️ Multiseat Manager GUI for Linux

A modern graphical interface for easily configuring and managing multiseat setups on Linux systems. Designed to simplify the process of assigning users, devices, and displays to multiple seats — without needing to use `loginctl` or write complex `udev` rules manually.

---

## 🎯 Purpose

Multiseat setups allow multiple users to share a single Linux system, each with their own monitor, keyboard, and mouse. This project provides a user-friendly GUI for:

- Viewing connected input/output devices
- Creating, updating, and removing seats
- Assigning or detaching devices from specific seats
- (Planned) AI-powered auto-configuration based on hardware profiles

---

## ✨ Features

- 🔌 Live device discovery (mouse, keyboard, display)
- 👤 CRUD operations for seat management
- 🧲 Easy device-seat linking/unlinking
- 📊 Seat/session overview (with TTY and seat ID info)
- 🤖 **(Experimental)**: AI-assisted autoconfig for optimal seat setup
- 🛡️ Built-in privilege escalation via `polkit` (optional)
- 💾 Config export for backup or deployment

---

## 🧱 Tech Stack

- **Python 3.13**
- **PyQt5** – for building the GUI
- `loginctl`, `udevadm` – for interacting with systemd and udev
- (Optional) `pyudev` – for live device detection
- `subprocess` – for shell command execution

---

## 🚀 Installation

### 1. Clone the repo
```bash
git clone https://github.com/your-username/multiseat-manager.git
cd multiseat-manager
