import RPi.GPIO as GPIO

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
        GPIO.setmode(GPIO.BCM)  # Używamy numeracji BCM
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
        GPIO.cleanup()
        print("Released all GPIO pins.")

    def cleanup(self):
        """
        Alias dla metody release (opcjonalnie, jeśli cleanup ma być bardziej intuicyjne).
        """
        self.release()
