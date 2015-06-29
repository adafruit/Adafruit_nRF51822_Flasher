import os
import subprocess
import platform
import click
import glob
import Platform
import sys

firmware_dir = 'Adafruit_BluefruitLE_Firmware'
openocd_dir = 'openocd-0.9.0'

openocd_dict = {'Windows': openocd_dir + '/win64/openocd.exe',
                'Darwin': 'openocd',
                'Ubuntu': openocd_dir + '/ubuntu/openocd',
                'RPi': openocd_dir + '/rpi/openocd',
                'RPi_native': openocd_dir + '/rpi_native/openocd'}

@click.command()
@click.option('--jtag', default='jlink', help='debugger must be "jlink" or "stlink" or "rpinative", default is "jlink"')
@click.option('--softdevice', default='8.0.0', help='Softdevice version e.g "8.0.0"')
@click.option('--bootloader', default=2, help='Bootloader version e.g "1" or "2".')
@click.option('--board', help='must be "blefriend32" or "blespislave".')
@click.option('--firmware', default='0.6.5', help='Firmware version e.g "0.6.5".')
def flash_nrf51(jtag, softdevice, bootloader, board, firmware):
    """Flash Bluefruit module Softdevice + Bootloader + Firmware"""
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
    if jtag == 'jlink':
        flash_status = subprocess.call('adalink nrf51822 --wipe --program ' + softdevice_hex + ' ' +
                                       bootloader_hex + ' ' +
                                       firmware_hex + ' ' + signature_hex, shell=True)
    elif (jtag == 'stlink') or (jtag == 'rpinative'):
        if (jtag == 'rpinative'):
            if (Platform.platform_detect() != Platform.RASPBERRY_PI):
                sys.exit()
            else:
                openocd_bin = openocd_dict['RPi_native']
                subprocess.call('chmod 755 ' + openocd_bin, shell=True)
                interface_cfg = 'raspberrypi' + ('2' if Platform.pi_version() == 2 else '') + '-native.cfg'
                interface_cfg = interface_cfg + ' -c "transport select swd" -c "set WORKAREASIZE 0"'
        else:
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
        print openocd_cmd
        flash_status = subprocess.call(openocd_cmd + ' -c init -c "reset init" -c halt -c "nrf51 mass_erase"' +
                                       ' -c "program ' + softdevice_hex + ' verify"' +
                                       ' -c "program ' + bootloader_hex + ' verify"' +
                                       ' -c "program ' + firmware_hex + ' verify"' +
                                       ' -c "program ' + signature_hex + ' verify"' +
                                       ' -c reset -c exit', shell=True)
    else:
        print 'unsupported debugger'

    if flash_status != 0:
        print "Flash FAILED"
    else:
        print "Flash OK"


if __name__ == '__main__':
    flash_nrf51()
