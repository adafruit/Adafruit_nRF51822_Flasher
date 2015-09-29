import os
import subprocess
import platform
import click
import glob
import Platform
import sys

supported_boards = ('blefriend32', 'blespifriend', 'blefriend16')
supported_programmers = ('jlink', 'stlink', 'rpigpio')

firmware_dir = 'Adafruit_BluefruitLE_Firmware'
openocd_dir = 'openocd-0.9.0'

openocd_dict = {'Windows': openocd_dir + '/win64/openocd.exe',
                'Darwin': 'openocd',
                'Ubuntu': openocd_dir + '/ubuntu/openocd',
                'RPi': openocd_dir + '/rpi/openocd',
                'RPi_gpio': openocd_dir + '/rpi_gpio/openocd'}

@click.command()
@click.option('--jtag', default='jlink', help='[Optional] debugger must be ' + ', '.join('"{0}"'.format(p) for p in supported_programmers) + ', default is "jlink"')
@click.option('--softdevice', default='8.0.0', help='[Optional] Softdevice version e.g "8.0.0"')
@click.option('--bootloader', default=2, help='[Optional] Bootloader version e.g "0" or "2".')
@click.option('--board', help='[Mandatory] must be ' + ', '.join('"{0}"'.format(b) for b in supported_boards))
@click.option('--firmware', help='[Mandatory] Firmware version e.g "0.6.5".')
def flash_nrf51(jtag, softdevice, bootloader, board, firmware):
    """Flash Bluefruit module Softdevice + Bootloader + Firmware"""

    if (board is None) or (board not in supported_boards):
        click.echo( "Please specify the board either " + ', '.join(supported_boards) )
        sys.exit(1)

    if (board == "blefriend16"):
        board = "blefriend"
        bootloader = 0 # force legacy bootloader

    if firmware is None:
        click.echo("Please specify the firmware version e.g: 0.6.5")
        sys.exit(1)

    if jtag not in supported_programmers:
        click.echo("Unsupported programmer, please specify one of following: " + ', '.join(supported_programmers))
        sys.exit(1)

    click.echo('jtag       \t: %s' % jtag)
    click.echo('softdevice \t: %s' % softdevice)
    click.echo('bootloader \t: %s' % bootloader)
    click.echo('board      \t: %s' % board)
    click.echo('firmware   \t: %s' % firmware)

    softdevice_hex = glob.glob(firmware_dir + '/softdevice/*' + softdevice + '_softdevice.hex')[0].replace('\\', '/')
    bootloader_hex = glob.glob(firmware_dir + '/bootloader/*' + str(bootloader) + '.hex')[0].replace('\\', '/')
    signature_hex = glob.glob(firmware_dir + '/' + firmware + '/' + board + '/*_signature.hex')[0].replace('\\', '/')
    firmware_hex = signature_hex.replace('_signature.hex', '.hex')

    click.echo('Writing Softdevice + DFU bootloader + Application to flash memory')
    if (jtag == 'jlink') or (jtag == 'stlink'):
        # click.echo('adalink -v nrf51822 --programmer ' + jtag +
        #                                 ' --wipe --program-hex "' + softdevice_hex + '"' +
        #                                 ' --program-hex "' + bootloader_hex + '"' +
        #                                 ' --program-hex "' + firmware_hex + '"' +
        #                                 ' --program-hex "' + signature_hex + '"')
        flash_status = subprocess.call('adalink nrf51822 --programmer ' + jtag +
                                       ' --wipe --program-hex "' + softdevice_hex + '"' +
                                       ' --program-hex "' + bootloader_hex + '"' +
                                       ' --program-hex "' + firmware_hex + '"' +
                                       ' --program-hex "' + signature_hex + '"', shell=True)
    elif (jtag == 'rpigpio'): # or (jtag == 'stlink'):
        if (jtag == 'rpigpio'):
            if (Platform.platform_detect() != Platform.RASPBERRY_PI):
                sys.exit()
            else:
                openocd_bin = openocd_dict['RPi_gpio']
                subprocess.call('chmod 755 ' + openocd_bin, shell=True)
                interface_cfg = 'raspberrypi' + ('2' if Platform.pi_version() == 2 else '') + '-native.cfg'
                interface_cfg = interface_cfg + ' -c "transport select swd" -c "set WORKAREASIZE 0"'
        else:
            interface_cfg = 'stlink-v2.cfg'
            if platform.system() != 'Linux':
                openocd_bin = openocd_dict[platform.system()]
            else:
                if Platform.platform_detect() == Platform.RASPBERRY_PI:
                    openocd_bin = openocd_dict['RPi']
                else:
                    openocd_bin = openocd_dict['Ubuntu']
                subprocess.call('chmod 755 ' + openocd_bin, shell=True)
                interface_cfg = 'stlink-v2.cfg'
        openocd_cmd = openocd_bin + ' -s ' + openocd_dir + '/scripts -l log.txt ' + '-f interface/' + interface_cfg + ' -f target/nrf51.cfg'
        flash_status = subprocess.call(openocd_cmd + ' -c init -c "reset init" -c halt -c "nrf51 mass_erase"' +
                                       ' -c "program ' + softdevice_hex + ' verify"' +
                                       ' -c "program ' + bootloader_hex + ' verify"' +
                                       ' -c "program ' + firmware_hex + ' verify"' +
                                       ' -c "program ' + signature_hex + ' verify"' +
                                       ' -c reset -c exit', shell=True if platform.system() != 'Windows' else False)
    else:
        click.echo('unsupported debugger')
        sys.exit()

    if flash_status != 0:
        print "Flash FAILED"
    else:
        print "Flash OK"


if __name__ == '__main__':
    flash_nrf51()
