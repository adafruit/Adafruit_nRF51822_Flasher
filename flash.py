import os
import subprocess
import platform
import click
import glob
import Platform

firmware_dir = 'Adafruit_BluefruitLE_Firmware'
openocd_dir = 'openocd-0.9.0'

openocd_dict = {'Windows': openocd_dir + '/win64/openocd.exe',
                'Darwin': 'openocd',
                'Ubuntu': openocd_dir + '/ubuntu/openocd',
                'RPi': openocd_dir + '/rpi/openocd'}

if platform.system() != 'Linux':
    openocd_bin = openocd_dict[platform.system()]
else:
    if Platform.platform_detect() == Platform.RASPBERRY_PI:
        openocd_bin = openocd_dict['RPi']
    else:
        openocd_bin = openocd_dict['Ubuntu']
    subprocess.call('chmod 755 ' + openocd_bin, shell=True)

OPENOCD_CMD = openocd_bin + ' -s ' + openocd_dir + '/scripts -l log.txt -f interface/stlink-v2.cfg -f target/nrf51.cfg'

@click.command()
@click.option('--jtag', default='jlink', help='debugger either is "jlink" or "stlink", default is "jlink"')
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
    elif jtag == 'stlink':
        flash_status = subprocess.call(OPENOCD_CMD + ' -c init -c "reset init" -c halt -c "nrf51 mass_erase"' +
                                       ' -c "program ' + softdevice_hex + ' verify"' +
                                       ' -c "program ' + bootloader_hex + ' verify"' +
                                       ' -c "program ' + firmware_hex + ' verify"' +
                                       ' -c "program ' + signature_hex + ' verify reset exit"', shell=True)
    else:
        print 'unsupported debugger'

    if flash_status != 0:
        print "Flash FAILED"
    else:
        print "Flash OK"


if __name__ == '__main__':
    flash_nrf51()
