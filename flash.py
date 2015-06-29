import os
import subprocess
import platform
import click
import intelhex
import glob

firmware_dir = 'Adafruit_BluefruitLE_Firmware'
BOOTLOADER_SETTING_ADDR = 0x3FC00
OCD_VERSION = '0.9.0'

if platform.system() == 'Windows':
    OPENOCD = 'openocd-' + OCD_VERSION + '/win64/openocd.exe'
elif platform.system() == 'Darwin':
    OPENOCD = 'openocd'
elif platform.system() == 'Linux':
    # assume Linux mean RPi
    OPENOCD = 'openocd-' + OCD_VERSION + '/rpi/openocd'
    subprocess.call('chmod 755 ' + OPENOCD)
else:
    print 'unsupported OS'

OPENOCD_CMD = OPENOCD + ' -s openocd-' + OCD_VERSION + '/scripts -l log.txt -f interface/stlink-v2.cfg -f target/nrf51.cfg'

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

    softdevice_hex = glob.glob( firmware_dir + '/softdevice/*' + softdevice + '_softdevice.hex' )[0].replace('\\', '/')
    bootloader_hex = glob.glob( firmware_dir + '/bootloader/*' + str(bootloader) + '.hex' )[0].replace('\\', '/')
    firmware_hex   = glob.glob( firmware_dir + '/' + firmware + '/' + board + '/*.hex' )[0].replace('\\', '/')
    signature_hex  = firmware_hex.replace('.hex', '_signature.hex')

    click.echo('Writing Softdevice + DFU bootloader + Application to flash memory')
    if jtag == 'jlink':
        flash_status = subprocess.call('adalink nrf51822 --wipe --program ' + softdevice_hex + ' ' +
                  bootloader_hex + ' ' +
                  firmware_hex + ' ' + signature_hex)
    elif jtag == 'stlink':
        flash_status = subprocess.call(OPENOCD_CMD + ' -c init -c "reset init" -c halt -c "nrf51 mass_erase"' +
                                                ' -c "program ' + softdevice_hex + ' verify"' +
                                                ' -c "program ' + bootloader_hex + ' verify"' +
                                                ' -c "program ' + firmware_hex   + ' verify"' +
                                                ' -c "program ' + signature_hex  + ' verify reset exit"' )
    else:
        print 'unsupported debugger'

    if flash_status != 0:
        print "Flash FAILED"
    else:
        print "Flash OK"

if __name__ == '__main__':
    flash_nrf51()