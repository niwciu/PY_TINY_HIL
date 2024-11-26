
from abc import ABC, abstractmethod

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
        # Devices should be grouped as {"protocols": [...], "peripherals": [...]}
        self.devices = devices
        self.logger = logger

    def initialize_all(self):
        for group, devices in self.devices.items():
            self.logger.log(f"\nInitializing {group}...", to_console=True)
            for device in devices:
                device.initialize()
                device_type = "Protocol" if isinstance(device, Protocol) else "Peripheral"
                self.logger.log(f"Initialized {type(device).__name__} ({device_type})", to_console=True)
            self.logger.log(f"All {group} initialized.", to_console=True)

    def release_all(self):
        for group, devices in self.devices.items():
            self.logger.log(f"\nReleasing {group}...", to_console=True)
            for device in devices:
                device.release()
                device_type = "Protocol" if isinstance(device, Protocol) else "Peripheral"
                self.logger.log(f"Released {type(device).__name__} ({device_type})", to_console=True)
            self.logger.log(f"All {group} released.", to_console=True)

    def get_device(self, group, name):
        if group in self.devices:
            for device in self.devices[group]:
                if type(device).__name__ == name:
                    return device
        raise ValueError(f"Device '{name}' not found in group '{group}'.")
