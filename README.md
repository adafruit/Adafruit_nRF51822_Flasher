# Adafruit_nRF51822_Flasher
Wrapper for the Segger J-Link or STLink/V2 (via OpenOCD) to flash nRF51822 MCUs

This tool provides a means to flash Bluefruit LE modules with the specified softdevice, bootloader, and firmware using a Segger J-Link or an STLink/V2 connected to the SWD port on the nRF51822.

This is useful if you need to de-brick a board that failed a DFU update, or some other unfortunate event.

## Requirements


### General Requirements
- One of the following SWD debuggers connected to the module via the SWD pins:
	- [Segger J-Link](https://www.adafruit.com/search?q=J-Link)
	- [STLink/V2](https://www.adafruit.com/product/2548)
- Perl (installation required for Windows, already available on OS X and Linux)
- [Adalink](https://github.com/adafruit/Adafruit_Adalink) installed on your system (A Python JLinkExe wrapper used to flash the device)
- [IntelHex](https://pythonhosted.org/IntelHex/index.html) Python library:
	- `sudo apt-get install python-pip`
	- `sudo pip install intelhex`

### STLink/V2 Requirements

To use the STLink/V2 you will also need OpenOCD. (See the [nRF51 OpenOCD Wiki Page](https://github.com/adafruit/Adafruit_nRF51822_Core/wiki/OpenOCD---STLink-V2) for further details).  On a Raspberry Pi the following steps are required:

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
perl flash.pl [--board] [--softdevice] [--bootloader] [--firmware]
  --jtag         debugger either is "jlink" or "stlink", default is "jlink"
  --board        board name, required, example is "blefriend32"
  --softdevice   SD version, default is "8.0.0"
  --bootloader   bootloader verion, default is "2"
  --firmware     firwmare verion,  required, example is "0.6.5"
```

`--firmware` and `--board` options are mandatory.

To flash the blefriend32 module using an STLink/V2 with SD 8.0.0, bootloader ver 2, firmware 0.6.5:

```
perl flash.pl --jtag=stlink --board=blefriend32 --softdevice=8.0.0 --bootloader=2 
--firmware=0.6.5
--jtag           "stlink"
--board          "blefriend32"
--softdevice     "8.0.0"
--bootloader     "2"
--firmware       "0.6.5"
Writing SoftDevice and merged DFU Bootload
```
