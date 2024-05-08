from tango import AttrWriteType, DispLevel, DevState
from tango.server import Device, attribute, command, device_property
import RPi.GPIO as GPIO


class RPiGPIO(Device):
    GPIO_PINS = device_property(dtype=(int,), mandatory=True, doc="GPIO pin number list")
    GPIO_LABELS = device_property(dtype=(str,), mandatory=True, doc="GPIO any desired label list")
    GPIO_MODES = device_property(dtype=(str,), mandatory=True, doc="GPIO modes list: IN or OUT")

    def initialize_dynamic_attributes(self):
        for gpio_label, gpio_mode in zip(self.GPIO_LABELS, self.GPIO_MODES):
            attr = attribute(
                name=gpio_label,
                label=gpio_label,
                dtype=bool,
                access=AttrWriteType.READ_WRITE if gpio_mode == "OUT" else AttrWriteType.READ,
                fget=self.gpio_read,
                fset=self.gpio_write if gpio_mode == "OUT" else None,
                memorized=True if gpio_mode == "OUT" else False,
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
        if self.validate_properties():
            # use internal chip numbering of GPIOs
            GPIO.setmode(GPIO.BCM)
            self.gpio_dict = dict(zip(self.GPIO_LABELS, self.GPIO_PINS))
            for gpio_pin, gpio_mode in zip(self.GPIO_PINS, self.GPIO_MODES):
                try:
                    GPIO.setup(gpio_pin, getattr(GPIO, gpio_mode))
                except Exception as e:
                    if isinstance(e, AttributeError):
                            self.error_stream(f"Invalid GPIO mode {gpio_mode}")
                    elif isinstance(e, ValueError):
                            self.error_stream(f"Invalid GPIO pin {gpio_pin}")
                    self.set_state(DevState.FAULT)
            self.initialize_dynamic_attributes()
            self.set_state(DevState.ON)
        else:
            self.error_stream("Non unique GPIO labels or/and GPIO pins")
            self.set_state(DevState.FAULT)

    @command
    def turn_off_all(self):
        for gpio_pin in self.GPIO_PINS:
            GPIO.output(gpio_pin, 0)

    @command
    def turn_on_all(self):
        for gpio_pin in self.GPIO_PINS:
            GPIO.output(gpio_pin, 1)

    def validate_properties(self):
        GPIO_LABELS = self.GPIO_LABELS
        GPIO_PINS = self.GPIO_PINS
        GPIO_MODES = self.GPIO_MODES
        if self.is_array_unique(GPIO_LABELS) and self.is_array_unique(GPIO_PINS):
            return len(GPIO_LABELS) == len(GPIO_PINS) == len(GPIO_MODES)
        else:
            return False

    def is_array_unique(self, array):
        return len(array) == len(set(array))

    def delete_device(self):
        Device.delete_device(self)
        self.turn_off_all()
        GPIO.cleanup()
