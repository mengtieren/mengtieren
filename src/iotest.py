
from pyftdi.gpio import (GpioAsyncController)


ssr_bank = GpioAsyncController()
ssr_bank.configure("ftdi:///2", direction=0xFF, frequency=1e3, initial=0x0)
opto_bank = GpioAsyncController()
opto_bank.configure("ftdi:///3", direction=0x00, frequency=1e3, initial=0x0)
gpio_bank = GpioAsyncController()
gpio_bank.configure("ftdi:///4", direction=0x00, frequency=1e3, initial=0x0)

#trigger
ssr_bank.write(0x01) 

#untrigger
ssr_bank.write(0x00) 


opto_input = opto_bank.read()






