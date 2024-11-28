from abc import ABC, abstractmethod
import sys


class Peripheral(ABC):
    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def release(self):
        pass


class Protocol(ABC):
    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def release(self):
        pass


class PeripheralManager:
    def __init__(self, devices, logger):
        """
        Zarządza urządzeniami i rezerwacjami GPIO.
        :param devices: Słownik z urządzeniami grupowanymi jako "protocols" i "peripherals".
        :param logger: Instancja klasy Logger do logowania.
        """
        self.devices = devices
        self.logger = logger
        self.gpio_registry = {}  # Rejestracja zajętych pinów w formacie {pin: "DeviceName"}
        self.initialized_devices = []  # Lista urządzeń zainicjalizowanych do momentu błędu

    def initialize_all(self):
        """
        Inicjalizuje wszystkie urządzenia w grupach 'protocols' i 'peripherals'.
        """
        for group, devices in self.devices.items():
            self.logger.log(f"\nInitializing {group}...", to_console=True)
            for device in devices:
                try:
                    pins = device.get_reserved_pins()  # Pobierz piny, które urządzenie chce zarezerwować
                    self._reserve_pins(pins, device.__class__.__name__)
                    device.initialize()
                    self._log_pins_initialized(pins, device.__class__.__name__)
                    self.initialized_devices.append(device)  # Dodaj urządzenie do listy zainicjalizowanych
                    self.logger.log(f"[INFO] {device.__class__.__name__} peripheral nitialized successfully.", to_console=True)
                except RuntimeError as e:
                    self.release_all()
                    self.logger.log(f"{str(e)}", to_console=True)
                    sys.exit(1)  # Zakończenie aplikacji
                except Exception as e:
                    self.logger.log(f"[ERROR] Unexpected error: {str(e)}", to_console=True)
                    self.release_all()
                    sys.exit(1)
            self.logger.log(f"All {group} initialized.", to_console=True)

    def release_all(self):
        """
        Zwalnia wszystkie urządzenia w grupach 'protocols' i 'peripherals'.
        """
        for device in self.initialized_devices:
            try:
                device.release()
                self.logger.log(f"[INFO] Released {device.__class__.__name__}.", to_console=True)
            except Exception as e:
                self.logger.log(f"[ERROR] Error during releasing {device.__class__.__name__}: {str(e)}", to_console=True)
        self.initialized_devices.clear()  # Czyszczenie listy zainicjalizowanych urządzeń
        self.gpio_registry.clear()  # Czyszczenie rejestru pinów
        self.logger.log("[INFO] All resources released.", to_console=True)

    def _reserve_pins(self, pins, device_name):
        """
        Rezerwuje piny GPIO dla urządzenia.
        :param pins: Lista pinów GPIO do zarezerwowania.
        :param device_name: Nazwa urządzenia rezerwującego piny.
        :raises RuntimeError: Jeśli którykolwiek pin jest już zajęty.
        """
        for pin in pins:
            if pin in self.gpio_registry:
                conflicting_device = self.gpio_registry[pin]
                self._log_conflict(pin, device_name, conflicting_device)
            self.gpio_registry[pin] = device_name
            self.logger.log(f"[INFO] Pin {pin} reserved for {device_name}.", to_console=True)

    def _log_conflict(self, pin, current_device, conflicting_device):
        """
        Loguje konflikt pinu i kończy działanie programu.
        :param pin: Numer pinu GPIO.
        :param current_device: Urządzenie próbujące zarezerwować pin.
        :param conflicting_device: Urządzenie, które już zarezerwowało pin.
        """
        message = (f"[ERROR] Pin {pin} conflict: {current_device} cannot be initialized "
                   f"because it is already reserved by {conflicting_device}.")
        self.logger.log(message, to_console=True)
        raise RuntimeError(message)

    def _log_pins_initialized(self, pins, device_name):
        """
        Loguje pomyślne zainicjalizowanie pinów.
        :param pins: Lista pinów.
        :param device_name: Nazwa urządzenia inicjalizującego piny.
        """
        for pin in pins:
            self.logger.log(f"[INFO] Pin {pin} successfully initialized by {device_name}.", to_console=True)

    def get_device(self, group, name):
        """
        Znajduje urządzenie na podstawie grupy (protocols/peripherals) i nazwy.
        :param group: Nazwa grupy ('protocols' lub 'peripherals').
        :param name: Nazwa klasy urządzenia (np. 'RPiGPIO').
        :return: Instancja urządzenia lub None, jeśli nie znaleziono.
        """
        if group in self.devices:
            for device in self.devices[group]:
                if type(device).__name__ == name:
                    return device
        raise ValueError(f"Device '{name}' not found in group '{group}'.")
