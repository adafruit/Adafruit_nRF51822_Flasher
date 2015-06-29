# Adafruit_nRF51822_Flasher
Wrapper for the Segger J-Link or STLink/V2 (via OpenOCD) to flash nRF51822 MCUs

This tool provides a means to flash Bluefruit LE modules with the specified softdevice, bootloader, and firmware using a Segger J-Link or an STLink/V2 connected to the SWD port on the nRF51822.

This is useful if you need to de-brick a board that failed a DFU update, or some other unfortunate event.

Since this repo includes [Adafruit_BluefruitLE_Firmware
](https://github.com/adafruit/Adafruit_BluefruitLE_Firmware) as a submodule, you will need to clone this with --recursive flag

	git clone --recursive git@github.com:adafruit/Adafruit_nRF51822_Flasher.git

If you already clone the repo with the Adafruit_BluefruitLE_Firmware as empty, you can still update the submodule by

	git submodule update --init --recursive

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

- git clone adalink, setup install adalink
- download install jlink driver

### STLink/V2 and RPi GPIO Requirements

To use the STLink/V2 or RPi GPIO you will also need OpenOCD. (See the [nRF51 OpenOCD Wiki Page](https://github.com/adafruit/Adafruit_nRF51822_Core/wiki/OpenOCD---STLink-V2) for further details).  On a Raspberry Pi the following steps are required:

Install libusb:

	sudo apt-get install libusb-dev libusb-1.0-0-dev

Configure UDEV permissions (you may need to log off or reboot):

	sudo cp openocd-0.9.0/contrib/99-openocd.rules /etc/udev/rules.d/
	sudo udevadm control --reload-rules

## Updating Git Submodules

The [Adafruit_BluefruitLE_Firmware](https://github.com/adafruit/Adafruit_BluefruitLE_Firmware) folder is setup as a git submodule, linked to an external repo.  If the folder is empty, you will need to run the following commands to fill it:

	git submodule init
	git submodule update

If you aren't operating from a git repo, you can fill the `Adafruit_BluefruitLE_Firmware` folder from the command-line with the following command:

	git clone git@github.com:adafruit/Adafruit_BluefruitLE_Firmware.git

## Usage

```
Usage: flash.py [OPTIONS]

  Flash Bluefruit module Softdevice + Bootloader + Firmware

Options:
  --jtag TEXT           debugger must be "jlink" or "stlink" or "rpinative",
                        default is "jlink"
  --softdevice TEXT     Softdevice version e.g "8.0.0"
  --bootloader INTEGER  Bootloader version e.g "1" or "2".
  --board TEXT          must be "blefriend32" or "blespislave".
  --firmware TEXT       Firmware version e.g "0.6.5".
  --help                Show this message and exit.
```

`--firmware` and `--board` options are mandatory.

To flash the blefriend32 module using an STLink/V2 with SD 8.0.0, bootloader ver 2, firmware 0.6.5:

	python flash.py --jtag=stlink --board=blefriend32 --softdevice=8.0.0 --bootloader=2 --firmware=0.6.5

To flash the above module with the same firmware using RPi GPIO
	
	python flash.py --jtag=rpinative --board=blefriend32 --softdevice=8.0.0 --bootloader=2 --firmware=0.6.5
