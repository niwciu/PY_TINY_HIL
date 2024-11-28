import RPi.GPIO as GPIO
from smbus2 import SMBus
import spidev
import serial


class RPiGPIO:
    def __init__(self, pin_config):
        """
        Klasa do obsługi GPIO.
        :param pin_config: Słownik w formacie {pin: {'mode': GPIO.OUT, 'initial': GPIO.LOW}}
        """
        self.pin_config = pin_config

    def get_required_resources(self):
        """
        Zwraca zasoby wymagane przez GPIO (lista pinów).
        """
        return {"pins": list(self.pin_config.keys())}

    def initialize(self):
        """
        Inicjalizuje piny GPIO.
        """
        GPIO.setmode(GPIO.BCM)
        for pin, config in self.pin_config.items():
            if config['mode'] == GPIO.OUT:
                GPIO.setup(pin, config['mode'], initial=config.get('initial', GPIO.LOW))
            else:
                GPIO.setup(pin, config['mode'])

    def release(self):
        """
        Zwalnia zarezerwowane piny GPIO.
        """
        for pin in self.pin_config.keys():
            GPIO.cleanup(pin)


class RPiPWM:
    def __init__(self, pin, frequency=1000):
        """
        Klasa do obsługi PWM.
        :param pin: Numer pinu GPIO.
        :param frequency: Częstotliwość PWM w Hz.
        """
        self.pin = pin
        self.frequency = frequency
        self.pwm = None

    def get_required_resources(self):
        """
        Zwraca zasoby wymagane przez PWM (lista pinów).
        """
        return {"pins": [self.pin]}

    def initialize(self):
        """
        Inicjalizuje PWM na pinie.
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, self.frequency)
        self.pwm.start(0)

    def set_duty_cycle(self, duty_cycle):
        """
        Ustawia wypełnienie PWM.
        :param duty_cycle: Wypełnienie w procentach (0-100).
        """
        if self.pwm:
            self.pwm.ChangeDutyCycle(duty_cycle)

    def release(self):
        """
        Zatrzymuje PWM i zwalnia pin.
        """
        if self.pwm:
            self.pwm.stop()
        GPIO.cleanup(self.pin)


class RPiUART:
    def __init__(self, port='/dev/serial0', baudrate=9600, timeout=1, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE):
        """
        Klasa do obsługi UART.
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.parity = parity
        self.stopbits = stopbits
        self.reserved_pins = [14, 15]  # Standardowe piny TXD i RXD
        self.serial = None

    def get_required_resources(self):
        """
        Zwraca zasoby wymagane przez UART (piny i port).
        """
        return {"pins": self.reserved_pins, "ports": [self.port]}

    def initialize(self):
        """
        Inicjalizuje port UART.
        """
        self.serial = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            timeout=self.timeout,
            parity=self.parity,
            stopbits=self.stopbits
        )

    def release(self):
        """
        Zamyka port UART.
        """
        if self.serial:
            self.serial.close()
            
    def get_initialized_params(self):
        """
        Zwraca parametry, z którymi zostały zainicjalizowane porty Modbus TRU.
        """
        return {
            "port": self.port,
            "baudrate": self.baudrate,
            "stopbits": self.stopbits,
            "parity": self.parity,
            "timeout": self.timeout
        }


class RPiI2C:
    def __init__(self, bus=1):
        """
        Klasa do obsługi magistrali I2C.
        """
        self.bus_number = bus
        self.reserved_pins = [2, 3]  # SDA i SCL dla I2C
        self.bus = None

    def get_required_resources(self):
        """
        Zwraca zasoby wymagane przez I2C (lista pinów).
        """
        return {"pins": self.reserved_pins}

    def initialize(self):
        """
        Inicjalizuje magistralę I2C.
        """
        self.bus = SMBus(self.bus_number)

    def release(self):
        """
        Zamyka magistralę I2C.
        """
        if self.bus:
            self.bus.close()


class RPiSPI:
    def __init__(self, bus=0, device=0):
        """
        Klasa do obsługi magistrali SPI.
        """
        self.spi = spidev.SpiDev()
        self.bus = bus
        self.device = device
        self.reserved_pins = [7, 8, 9, 10, 11]  # CE0, CE1, MISO, MOSI, SCLK

    def get_required_resources(self):
        """
        Zwraca zasoby wymagane przez SPI (lista pinów).
        """
        return {"pins": self.reserved_pins}

    def initialize(self):
        """
        Otwiera połączenie SPI.
        """
        self.spi.open(self.bus, self.device)

    def release(self):
        """
        Zamyka połączenie SPI.
        """
        self.spi.close()


# Nowe klasy peryferiów
class RPi1Wire:
    def __init__(self, pin):
        self.pin = pin

    def get_required_resources(self):
        return {"pins": [self.pin]}

    def initialize(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)

    def release(self):
        GPIO.cleanup(self.pin)


class RPiADC:
    def __init__(self, channel):
        self.channel = channel
        self.spi = spidev.SpiDev()

    def get_required_resources(self):
        return {"pins": [7, 8, 9, 10, 11]}  # Standardowe piny SPI

    def initialize(self):
        self.spi.open(0, self.channel)
        self.spi.max_speed_hz = 1350000

    def read(self):
        adc = self.spi.xfer2([1, (8 + self.channel) << 4, 0])
        return ((adc[1] & 3) << 8) + adc[2]

    def release(self):
        self.spi.close()


class RPiCAN:
    def __init__(self, interface='can0'):
        self.interface = interface

    def get_required_resources(self):
        return {"pins": []}  # CAN zwykle nie używa GPIO

    def initialize(self):
        import os
        os.system(f'sudo ip link set {self.interface} up type can bitrate 500000')

    def release(self):
        import os
        os.system(f'sudo ip link set {self.interface} down')


class RPiHATEEPROM:
    def __init__(self, bus=1, address=0x50):
        self.bus_number = bus
        self.address = address
        self.bus = None

    def get_required_resources(self):
        return {"pins": [2, 3]}  # SDA i SCL

    def initialize(self):
        self.bus = SMBus(self.bus_number)

    def read_eeprom(self, offset, length):
        return [self.bus.read_byte_data(self.address, offset + i) for i in range(length)]

    def release(self):
        if self.bus:
            self.bus.close()


class RPiHardwarePWM:
    def __init__(self, pin, frequency=1000):
        self.pin = pin
        self.frequency = frequency

    def get_required_resources(self):
        return {"pins": [self.pin]}

    def initialize(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

    def release(self):
        GPIO.cleanup(self.pin)
