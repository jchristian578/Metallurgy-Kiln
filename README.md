# Metallurgy-Kiln
## Installation Guide

This guide assumes you are installing the controller on a Raspberry Pi running Raspberry Pi OS (Bullseye or Bookworm) with Python 3.11.

### Phase 1: Hardware Preparation

Before installing the software, ensure your Raspberry Pi is configured to communicate with the hardware sensors.

1. **Enable Interfaces:** Open the Raspberry Pi configuration tool.
```bash
sudo raspi-config

```


2. Navigate to **Interface Options**.
3. Enable **SPI** (required for the MAX31856 Thermocouple amplifier).
4. Enable **I2C** (required if you are using the 20x4 LCD display).
5. Exit and reboot the Pi.

### Phase 2: System Dependencies

Update your system and install the necessary Python environment tools.

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv git i2c-tools -y

```

### Phase 3: Install Required Libraries

Because modern Raspberry Pi OS restricts global pip installations, it is recommended to use the system package manager for hardware libraries where possible, and pip for the rest using the override flag.

```bash
# Install hardware control libraries via apt (Safest for Bookworm OS)
sudo apt install python3-gpiozero python3-rpi.gpio -y

# Install the web server, sensor drivers, and math libraries via pip
sudo python3.11 -m pip install fastapi uvicorn adafruit-circuitpython-max31856 board pydantic --break-system-packages

```

### Phase 4: Download and Configure

1. Move the `MetallurgyKiln` project folder to your home directory (e.g., `/home/pi/MetallurgyKiln` or `/home/pi/MetallurgyKiln`).
2. Open the `config.py` file to set your specific hardware pins and network settings.
```bash
nano ~/MetallurgyKiln/config.py

```


3. **Crucial Settings to Check:**
* `WEB_PORT`: Usually `80` (requires `sudo` to run) or `5000`.
* `CS_PIN`: The GPIO pin connected to your MAX31856 Chip Select.
* `RELAY_1_PIN` / `RELAY_2_PIN`: The GPIO pins controlling your Solid State Relays.
* `KILN_WATTAGE_W`: Set this to your kiln's wattage for accurate cost estimations.
* *Save and exit (CTRL+O, Enter, CTRL+X).*



### Phase 5: Run on Boot (Systemd Service)

To ensure the kiln controller starts automatically when the Pi receives power, create a service file.

1. Create the service file:
```bash
sudo nano /etc/systemd/system/kiln.service

```


2. Paste the following configuration (adjust the `WorkingDirectory` and `ExecStart` paths to match your username):
```ini
[Unit]
Description=Metallurgy Kiln Controller V2
After=network.target

[Service]
User=root
WorkingDirectory=/home/pi/MetallurgyKiln
ExecStart=/usr/bin/python3.11 /home/pi/MetallurgyKiln/server.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target

```


3. Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable kiln.service
sudo systemctl start kiln.service

```



---

## User Guide

Access the interface by typing the Raspberry Pi's IP address into the web browser of any device on the same Wi-Fi network (e.g., `[http://192.168.1.110](http://192.168.1.110)`).

<img width="1443" height="817" alt="kiln" src="https://github.com/user-attachments/assets/c54b79d1-0082-45cf-bd07-250fdea68415" />

<img width="661" height="424" alt="graph" src="https://github.com/user-attachments/assets/2c860cee-62e7-409e-8c72-0371e6835f01" />

### The Run Card (Monitoring & Control)

This card gives you real-time insight into the physical state of the kiln.

* **Thermocouple:** Displays the current internal temperature.
* **Setpoint:** Displays the target temperature the controller is currently trying to achieve.
* **Relay Duty (%):** Shows how much power is being applied. 100% means the relay is locked on, 50% means it pulses on and off equally. If the text is red, it is actively heating; if blue, it is coasting/cooling.
* **Quick Soak:** Instantly ramps the kiln to a specific temperature and holds it there for a set duration. Useful for drying out the kiln or pre-heating without saving a permanent profile.
* **Stop:** Immediately cuts power to the relays and aborts the current run.

### The Profile Builder

The builder allows you to design multi-step firing schedules. Profiles are built row by row.

#### Ramp vs. Soak

Every step handles both getting to a temperature and holding it.

* **Target:** The temperature you want to reach.
* **Duration:** How long to stay at that target temperature *after* it has been reached.
* **Rate:** How fast the kiln should heat or cool to reach the target.

#### Rate Controls (M vs S)

* **M (Max Rate):** The controller will apply 100% power to heat up (or 0% power to cool down) as fast as the physical kiln is capable of.
* **S (Set Rate):** You define a specific speed (e.g., 30°C/minute). The controller will strictly govern the temperature to follow this curve.

#### Saving and Starting

* **Show Graph:** Opens a preview window to verify your curve before saving.
* **Save Profile:** Writes the profile to disk. You must give it a name in the top input box.
* **Start Profile:** Begins the firing schedule immediately.

### The Graphing Engine

The live graph tracks the physical temperature against your planned schedule.

* **Views:** Toggle between **Profile Run** (zoomed in on the current firing) and **Total Run** (includes all data since the controller was powered on).
* **Lines:**
* **Solid White:** The actual physical temperature.
* **Dashed White:** The controller's current Setpoint (what it is aiming for right now).
* **Solid Blue (Planned):** The theoretical path the profile should take. If the solid white line falls behind the blue line, your kiln is struggling to keep up with the requested rate.



### Physical Aux Buttons

If configured in `config.py`, up to four physical buttons can be wired to the controller.

* Press and hold a button for 2 seconds (the default safety delay) to instantly start its assigned profile.
* The web interface mirrors these buttons under the Run card. They turn gold/orange when assigned.
* Aux buttons are disabled while the kiln is actively running to prevent accidental profile switching mid-fire.

### Safety & Auto-Resume

* **Power Loss Recovery:** If power is cut mid-firing, the system saves its exact state. When power returns, it waits 30 seconds for sensors to stabilize. If the power was out for less than 20 minutes and the kiln lost less than 50°C, it will automatically resume the profile exactly where it left off. You will see a red notification modal acknowledging the recovery.
* **Guaranteed Soak:** If you ask the kiln to heat at 100°C/min, but it can physically only achieve 50°C/min, the clock will pause. It will not begin counting down the "Soak" timer until the actual temperature is within 15°C of the target.
* **Open Loop Detection:** If the system applies 100% power for several minutes but the temperature does not rise, it assumes a broken heating element or a disconnected thermocouple and will shut down automatically.
