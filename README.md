# Adafruit nRF51822 Flasher

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [Requirements](#requirements)
  - [General Requirements](#general-requirements)
  - [Jlink Requirements](#jlink-requirements)
  - [STLink/V2 Requirements](#stlinkv2-requirements)
  - [RPi GPIO Requirements](#rpi-gpio-requirements)
- [Usage](#usage)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

The flasher utility is a wrapper for various debuggers to flash nRF51822 MCUs with the official Adafruit firmware images.  Currently supported debuggers are:

- [Segger J-Link](https://www.adafruit.com/search?q=J-Link) (via [Adalink](https://github.com/adafruit/Adafruit_Adalink))
- [STLink/V2](https://www.adafruit.com/product/2548) (via OpenOCD, included in this repo)
- Raspberry Pi GPIO (via OpenOCD, included in this repo)

This tool hides the implementation details of the different debuggers, and provides a means to flash Bluefruit LE modules with the specified softdevice, bootloader, and firmware via the SWD pins on the nRF51822 (SWDIO and SWCLK).

This is useful if you need to de-brick a board that failed a DFU update, or some other unfortunate event.

The [Adafruit_BluefruitLE_Firmware](https://github.com/adafruit/Adafruit_BluefruitLE_Firmware) folder is setup as a git submodule, linked to an external repo. you will need to clone this with --recursive flag

	git clone --recursive git@github.com:adafruit/Adafruit_nRF51822_Flasher.git

If the folder is empty, you will need to run the following commands to fill it:

	git submodule init
	git submodule update

If you aren't operating from a git repo, you can fill the `Adafruit_BluefruitLE_Firmware` folder from the command-line with the following command:

	git clone git@github.com:adafruit/Adafruit_BluefruitLE_Firmware.git

## Requirements

### General Requirements
- One of the following SWD debuggers connected to the module via the SWD pins:
	- [Segger J-Link](https://www.adafruit.com/search?q=J-Link)
	- [STLink/V2](https://www.adafruit.com/product/2548)
	- Raspberry Pi GPIO
- [Adalink](https://github.com/adafruit/Adafruit_Adalink) installed on your system (A Python JLinkExe wrapper used to flash the device)
- [click](http://click.pocoo.org/4/) Python library:
	- `sudo apt-get install python-pip`
	- `sudo pip install click`

### Jlink Requirements

- git clone adalink
- install and setup adalink
- download and install jlink driver

### STLink/V2 Requirements

To use the STLink/V2 you will also need OpenOCD. Pre-built binaries is provided in `openocd-x.x.x` for Windows, Ubuntu, and RPi. If your system is not one of these options, you can build it by yourself following **TODO: create a how-to-build-openocd-md**.

On Linux or Raspberry Pi the following steps are required:

Install libusb:

	sudo apt-get install libusb-dev libusb-1.0-0-dev

Configure UDEV permissions:

	sudo cp openocd-0.9.0/contrib/99-openocd.rules /etc/udev/rules.d/
	sudo udevadm control --reload-rules

Then reboot.

**STLink/V2 to Bluefruit LE Pinout**

The following pins on the STLink/V2 need to be connected to the Bluefruit LE module:

STLink/V2 | Bluefruit LE
--------- | --------
RST       | RST
SWCLK     | SWCLK
SWDIO     | SWDIO
GND       | GND
3.3V      | VIN

### RPi GPIO Requirements

You can use the RPi's raw GPIO to bit-bang JTAG/SWD signals, turning your RPi into a native debugger.  A pre-built binary is included in the `openocd-x.x.x/rpi_gpio/openocd` folder.

Install libusb:

	sudo apt-get install libusb-dev libusb-1.0-0-dev

Since accessing RPi's GPIO requires root access, sudo is required when executing the `flash.py` script:

**RPi 1 wiring**

![rpi_openocd_swd](https://cloud.githubusercontent.com/assets/249515/8418755/52657200-1edf-11e5-880f-4d80496e725e.png)

**RPi 2 wiring**

![rpi2_swd.png](https://cloud.githubusercontent.com/assets/249515/8327921/59465064-1a96-11e5-802f-827d6707686e.png)

NOTE: Don't forget to connect GND, meaning that there are 4 wires in total.

## Usage

```
Usage: flash.py [OPTIONS]

  Flash Bluefruit module Softdevice + Bootloader + Firmware

Options:
  --jtag TEXT           debugger must be "jlink" or "stlink" or "rpigpio",
                        default is "jlink"
  --softdevice TEXT     Softdevice version e.g "8.0.0"
  --bootloader INTEGER  Bootloader version e.g "1" or "2".
  --board TEXT          must be "blefriend32" or "blespifriend".
  --firmware TEXT       Firmware version e.g "0.6.5".
  --help                Show this message and exit.
```

`--firmware` and `--board` options are mandatory.

To flash the blefriend32 module using an STLink/V2 with SD 8.0.0, bootloader ver 2, firmware 0.6.5:

	python flash.py --jtag=stlink --board=blefriend32 --softdevice=8.0.0 --bootloader=2 --firmware=0.6.5

To flash the above module with the same firmware using RPi GPIO
	
	sudo python flash.py --jtag=rpigpio --board=blefriend32 --softdevice=8.0.0 --bootloader=2 --firmware=0.6.5
