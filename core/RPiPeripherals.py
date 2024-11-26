import RPi.GPIO as GPIO
import serial
import smbus2
import spidev
from smbus2 import SMBus


class RPiGPIO:
    def __init__(self, pin_config):
        """
        Inicjalizuje wiele pinów GPIO.
        :param pin_config: Słownik w formacie {pin: {'mode': GPIO.OUT, 'initial': GPIO.LOW}}
        """
        self.pin_config = pin_config

    def initialize(self):
        """
        Inicjalizuje wszystkie piny GPIO.
        """
        GPIO.setmode(GPIO.BCM)  # Ustaw tryb numeracji pinów
        for pin, config in self.pin_config.items():
            if config['mode'] == GPIO.OUT:
                GPIO.setup(pin, config['mode'], initial=config.get('initial', GPIO.LOW))
            else:
                GPIO.setup(pin, config['mode'])
            print(f"Initialized GPIO pin {pin} as {'OUTPUT' if config['mode'] == GPIO.OUT else 'INPUT'}.")

    def write(self, pin, value):
        """
        Ustawia stan konkretnego pinu GPIO.
        :param pin: Numer pinu GPIO.
        :param value: GPIO.HIGH lub GPIO.LOW.
        """
        if self.pin_config[pin]['mode'] != GPIO.OUT:
            raise RuntimeError(f"Cannot write to pin {pin}. It must be set as OUTPUT.")
        GPIO.output(pin, value)

    def read(self, pin):
        """
        Odczytuje stan konkretnego pinu GPIO.
        :param pin: Numer pinu GPIO.
        :return: GPIO.HIGH lub GPIO.LOW.
        """
        if self.pin_config[pin]['mode'] != GPIO.IN:
            raise RuntimeError(f"Cannot read from pin {pin}. It must be set as INPUT.")
        return GPIO.input(pin)

    def release(self):
        """
        Zwolnij wszystkie zasoby GPIO.
        """
        GPIO.setmode(GPIO.BCM)  # Ustaw tryb numeracji pinów przed cleanup
        for pin in self.pin_config.keys():
            GPIO.cleanup(pin)
            print(f"Released GPIO pin {pin}.")

class RPiPWM:
    def __init__(self, pin, frequency=1000):
        """
        Inicjalizuje PWM na określonym pinie.
        :param pin: Numer pinu GPIO.
        :param frequency: Częstotliwość PWM w Hz.
        """
        self.pin = pin
        self.frequency = frequency
        self.pwm = None

    def initialize(self):
        """
        Inicjalizuje PWM na pinie.
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, self.frequency)
        self.pwm.start(0)  # Rozpoczyna PWM z wypełnieniem 0%.
        print(f"Initialized PWM on pin {self.pin} with frequency {self.frequency}Hz.")

    def set_duty_cycle(self, duty_cycle):
        """
        Ustawia wypełnienie sygnału PWM.
        :param duty_cycle: Wypełnienie w procentach (0-100).
        """
        if self.pwm:
            self.pwm.ChangeDutyCycle(duty_cycle)

    def stop(self):
        """
        Zatrzymuje PWM.
        """
        if self.pwm:
            self.pwm.stop()

    def release(self):
        """
        Zwolnij zasoby PWM.
        """
        self.stop()
        GPIO.cleanup(self.pin)
        print(f"Released PWM on pin {self.pin}.")


class RPiUART:
    def __init__(self, port='/dev/serial0', baudrate=9600, timeout=1):
        """
        Inicjalizuje UART.
        :param port: Port UART (domyślnie '/dev/serial0').
        :param baudrate: Prędkość transmisji w baudach.
        :param timeout: Timeout transmisji w sekundach.
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial = None

    def initialize(self):
        """
        Inicjalizuje port UART.
        """
        self.serial = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
        print(f"Initialized UART on port {self.port} with baudrate {self.baudrate}.")

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
        Zamykamy port UART.
        """
        if self.serial:
            self.serial.close()
        print(f"Released UART on port {self.port}.")


class RPiI2C:
    def __init__(self, bus=1):
        """
        Inicjalizuje magistralę I2C.
        :param bus: Numer magistrali I2C (domyślnie 1).
        """
        self.bus_number = bus
        self.bus = None

    def initialize(self):
        """
        Otwiera magistralę I2C.
        """
        self.bus = SMBus(self.bus_number)
        print(f"Initialized I2C bus {self.bus_number}.")

    def write_byte(self, address, value):
        """
        Wysyła pojedynczy bajt przez I2C.
        :param address: Adres urządzenia I2C.
        :param value: Bajt do wysłania.
        """
        if self.bus:
            self.bus.write_byte(address, value)

    def read_byte(self, address):
        """
        Odczytuje pojedynczy bajt przez I2C.
        :param address: Adres urządzenia I2C.
        :return: Odebrany bajt.
        """
        if self.bus:
            return self.bus.read_byte(address)

    def release(self):
        """
        Zamykamy magistralę I2C.
        """
        if self.bus:
            self.bus.close()
            print(f"Released I2C bus {self.bus_number}.")


class RPiSPI:
    def __init__(self, bus=0, device=0):
        """
        Inicjalizuje magistralę SPI.
        :param bus: Numer magistrali SPI (domyślnie 0).
        :param device: Numer urządzenia SPI (domyślnie 0).
        """
        self.spi = spidev.SpiDev()
        self.bus = bus
        self.device = device

    def initialize(self):
        """
        Otwiera połączenie SPI.
        """
        self.spi.open(self.bus, self.device)
        print(f"Initialized SPI on bus {self.bus}, device {self.device}.")

    def transfer(self, data):
        """
        Wysyła i odbiera dane przez SPI.
        :param data: Dane do wysłania (lista bajtów).
        :return: Odebrane dane (lista bajtów).
        """
        return self.spi.xfer(data)

    def release(self):
        """
        Zamykamy połączenie SPI.
        """
        self.spi.close()
        print("Released SPI.")