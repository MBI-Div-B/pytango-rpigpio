from tango import AttrWriteType, DispLevel, DevState
from tango.server import Device, attribute, command, device_property
from enum import IntEnum
import RPi.GPIO as GPIO


class RPiGPIO(Device):
    GPIO_PINS = device_property(dtype=(int,), mandatory=True)
    GPIO_LABELS = device_property(dtype=(str,), mandatory=True)

    def initialize_dynamic_attributes(self):
        for gpio_label in self.GPIO_LABELS:
            attr = attribute(
                name=gpio_label,
                label=gpio_label,
                dtype=bool,
                access=AttrWriteType.READ_WRITE,
                fget=self.gpio_read,
                fset=self.gpio_write,
                memorized=True,
            )
            self.add_attribute(attr)

    def gpio_read(self, attr):
        attr_name = attr.get_name()
        gpio_id = self.gpio_dict.get(attr_name)
        if gpio_id is not None:
            value = bool(GPIO.input(gpio_id))
            return value

    def gpio_write(self, attr):
        attr_name = attr.get_name()
        gpio_id = self.gpio_dict.get(attr_name)
        value = attr.get_write_value()
        if gpio_id is not None:
            GPIO.output(gpio_id, value)

    def init_device(self):
        Device.init_device(self)
        GPIO.setmode(GPIO.BOARD)
        self.gpio_dict = dict(zip(self.GPIO_LABELS, self.GPIO_PINS))
        for gpio_pin in self.GPIO_PINS:
            GPIO.setup(gpio_pin, GPIO.OUT)
        self.set_state(DevState.ON)
