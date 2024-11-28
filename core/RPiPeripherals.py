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

    def get_reserved_pins(self):
        """
        Zwraca listę pinów, które urządzenie chce zarezerwować.
        """
        return list(self.pin_config.keys())

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

    def get_reserved_pins(self):
        """
        Zwraca listę pinów, które urządzenie chce zarezerwować.
        """
        return [self.pin]

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
        :param port: Port UART (domyślnie '/dev/serial0').
        :param baudrate: Prędkość transmisji w baudach.
        :param timeout: Timeout transmisji w sekundach.
        :param parity: Parzystość ('serial.PARITY_NONE', 'serial.PARITY_ODD', 'serial.PARITY_EVEN').
        :param stopbits: Liczba bitów stopu ('serial.STOPBITS_ONE', 'serial.STOPBITS_TWO').
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.parity = parity
        self.stopbits = stopbits
        self.reserved_pins = [14, 15]  # Standardowe piny TXD i RXD
        self.serial = None

    def get_reserved_pins(self):
        """
        Zwraca listę pinów, które urządzenie chce zarezerwować.
        """
        return self.reserved_pins

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

    def send(self, data):
        """
        Wysyła dane przez UART.
        :param data: Dane do wysłania (bytes).
        """
        if self.serial:
            self.serial.write(data)

    def receive(self):
        """
        Odbiera dane przez UART.
        :return: Odebrane dane (bytes).
        """
        if self.serial:
            return self.serial.read_all()

    def release(self):
        """
        Zamyka port UART.
        """
        if self.serial:
            self.serial.close()


class RPiI2C:
    def __init__(self, bus=1):
        """
        Klasa do obsługi magistrali I2C.
        :param bus: Numer magistrali I2C (domyślnie 1).
        """
        self.bus_number = bus
        self.reserved_pins = [2, 3]  # SDA i SCL dla I2C
        self.bus = None

    def get_reserved_pins(self):
        """
        Zwraca listę pinów, które urządzenie chce zarezerwować.
        """
        return self.reserved_pins

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
        :param bus: Numer magistrali SPI (domyślnie 0).
        :param device: Numer urządzenia SPI (domyślnie 0).
        """
        self.spi = spidev.SpiDev()
        self.bus = bus
        self.device = device
        self.reserved_pins = [7, 8, 9, 10, 11]  # CE0, CE1, MISO, MOSI, SCLK

    def get_reserved_pins(self):
        """
        Zwraca listę pinów, które urządzenie chce zarezerwować.
        """
        return self.reserved_pins

    def initialize(self):
        """
        Otwiera połączenie SPI.
        """
        self.spi.open(self.bus, self.device)

    def transfer(self, data):
        """
        Przesyła dane przez SPI.
        :param data: Dane do wysłania (lista bajtów).
        :return: Odebrane dane (lista bajtów).
        """
        return self.spi.xfer(data)

    def release(self):
        """
        Zamyka połączenie SPI.
        """
        self.spi.close()
