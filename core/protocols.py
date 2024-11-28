from pymodbus.client import ModbusSerialClient as ModbusClient
from abc import ABC, abstractmethod


class Protocol(ABC):
    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def release(self):
        pass


class ModbusTRU(Protocol):
    def __init__(self, port='/dev/ttyUSB0', baudrate=115200, stopbits=1, parity='N', timeout=1):
        """
        Klasa do obsługi Modbus RTU.
        :param port: Port szeregowy do komunikacji.
        :param baudrate: Szybkość transmisji w baudach.
        :param stopbits: Liczba bitów stopu.
        :param parity: Parzystość ('N', 'E', 'O').
        :param timeout: Czas oczekiwania na odpowiedź w sekundach.
        """
        self.port = port
        self.baudrate = baudrate
        self.stopbits = stopbits
        self.parity = parity
        self.timeout = timeout
        self.client = None

    def get_required_resources(self):
        """
        Zwraca zasoby wymagane przez Modbus RTU (port szeregowy).
        """
        return {"ports": [self.port]}

    def initialize(self):
        """
        Inicjalizuje klienta Modbus RTU.
        """
        self.client = ModbusClient(
            port=self.port,
            baudrate=self.baudrate,
            stopbits=self.stopbits,
            parity=self.parity,
            timeout=self.timeout
        )
        if not self.client.connect():
            raise ConnectionError(f"Unable to connect to Modbus RTU server on port {self.port}.")

    def release(self):
        """
        Zamyka połączenie Modbus RTU.
        """
        if self.client:
            self.client.close()
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


    def read_holding_registers(self, slave_address, address, count):
        """
        Odczytuje rejestry holding z urządzenia Modbus RTU.
        :param slave_address: Adres urządzenia slave.
        :param address: Adres początkowego rejestru.
        :param count: Liczba rejestrów do odczytania.
        :return: Lista wartości rejestrów.
        """
        response = self.client.read_holding_registers(address, count, slave=slave_address)
        if response.isError():
            raise ValueError(f"Modbus error: {response}")
        return response.registers

    def write_single_register(self, slave_address, address, value):
        """
        Zapisuje pojedynczy rejestr w urządzeniu Modbus RTU.
        :param slave_address: Adres urządzenia slave.
        :param address: Adres rejestru.
        :param value: Wartość do zapisania.
        :return: Odpowiedź z urządzenia.
        """
        response = self.client.write_register(address, value, slave=slave_address)
        if response.isError():
            raise ValueError(f"Modbus error: {response}")
        return response

    def write_multiple_registers(self, slave_address, address, values):
        """
        Zapisuje wiele rejestrów w urządzeniu Modbus RTU.
        :param slave_address: Adres urządzenia slave.
        :param address: Adres początkowego rejestru.
        :param values: Lista wartości do zapisania.
        :return: Odpowiedź z urządzenia.
        """
        response = self.client.write_registers(address, values, slave=slave_address)
        if response.isError():
            raise ValueError(f"Modbus error: {response}")
        return response
