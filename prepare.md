# Prepare the Raspberry Pi Zero

This description is commen for alle variants of clocks. Replace the 'XXX' with the clock name (e.g. 'bcd')

* Download RASPBIAN image and flash to MicroSD card
  * See: https://www.raspberrypi.org/downloads/

* Change boot files on MicroSD card for headless NDIS (USB/Ethernet) connection
  * See: http://www.circuitbasics.com/raspberry-pi-zero-ethernet-gadget/   or
  https://www.factoryforward.com/pi-zero-w-headless-setup-windows10-rndis-driver-issue-resolved/


* Boot Raspberry Pi (can take more than a minute at first time)

* Use SSH to connect to `raspberrypi.local`
  * Note: On Windows system use program Putty
  * Note: NDIS setup a network with address 169.254.*.*/16. It can take several minutes til the DNS entry is available

* Login with user `pi` and password `raspberry`

* Use `sudo raspi-config` to configure RPi system:
  * Set new password in menu `Change User Password`
  * Change device name in menu `Network Options` -> `Hostnames` (e.g. 'RPiClock')
  * Set WIFI access to your local network. Set SSID and key in menu `Network Options` -> `WIFI`
  * Set Localization in menu `Localozation Options` -> `Change Locale`
  * Set Timezone in menu `Localization Options` -> `Timezone`
  * (optional) Enable I2C if needed in menu `Interfacing Options` -> `I2C`
  * (optional) Enable 1-Wire if needed in menu `Interfacing Options` -> `1-Wire`
  * Note: If using GPIO xx, do NOT enable SPI 

* Update your RPi system with `sudo apt-get update` and `sudo apt-get upgrade`

* Install additional programs and libs with:
  * `sudo apt-get install python3 python3-pip`
  * `sudo apt-get install pigpio`
  * `sudo apt-get install git`

* Start pigpio deamon with `sudo systemctl start pigpiod`

* Start pigpio deamon at next boot automatically with `sudo systemctl enable pigpiod`

* Install additional python libs with:
  * `pip3 install pigpio` and/or? `sudo pip3 install pigpio`

* Download clock repository from GITHUB with `git clone https://github.com/fablab-wue/piClock.git`

* Make python file executable with `sudo chmod +x /home/pi/piClock/XXX.py`

* Test if clock program is working
  * Start clock with `/home/pi/piClock/XXX.py`
  * Stop with Ctrl-C

* Variant 1 - Prepare system to start clock program at startup
  * Edit rc.local with `sudo nano /etc/rc.local`
  * Add at end before `exit 0` `sudo /home/pi/piClock/XXX.py &`

* Variant 2 - Prepare system to start clock program at startup
  * Edit system crontab file with `sudo crontab -e`
  * Add at end `@reboot /home/pi/piClock/XXX.py`


* If all works, make a backup of the MicroSD card