# pytango-rpigpio
This tangoDS allows to control the outputs (LOW/HIGH) of raspberry GPIOs.

## Installation
This tangoDS uses the python packaging. So you can easily install this software using `pip`.

Just run 

`pip(3) install .`

and it will install the necessary dependencies.
## Configuration
In order to use this tangoDS you need to specify the occupied GPIO of RaspbrerryPi in the `GPIO_PINS` tangoDS property and assign unique labels in `GPIO_LABELS` tangoDS property in the same order.

You can see the pinout of RaspberryPI GPIO in the picture below:
![](doc/gpio-pinout.png)
The TangoDS uses the internal GPIO numbering of the Broadcom chip as set by the command

`GPIO.setmode(GPIO.BCM) . `

## Authors
Leonid Lunin
