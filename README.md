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
This project structure is inspired by the MVC model, with models for a seat, session and a device and an interface for MultiseatManager,
the SystemdMultiseatManager implement this interface. I plan to refine the code later so the view is agnostic to the exact implementation, but that seems unnecessary for now as I am sorely focused on linux.

## 🚀 Installation
(To be added)
