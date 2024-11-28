from pymodbus.client import ModbusSerialClient as ModbusClient
from abc import ABC, abstractmethod


class Protocol(ABC):
    """
    Interfejs dla protokołów komunikacyjnych.
    """
    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def release(self):
        pass


class ModbusTRU(Protocol):
    """
    Klasa obsługująca protokół Modbus RTU.
    """
    def __init__(self, port='/dev/ttyUSB0', baudrate=115200, stopbits=1, parity='N', timeout=1):
        """
        Inicjalizuje parametry komunikacji Modbus RTU.
        :param port: Port szeregowy (np. '/dev/ttyUSB0').
        :param baudrate: Prędkość transmisji w bitach na sekundę.
        :param stopbits: Ilość bitów stopu (1 lub 2).
        :param parity: Parzystość ('N' - brak, 'E' - parzysta, 'O' - nieparzysta).
        :param timeout: Timeout w sekundach.
        """
        self.port = port
        self.baudrate = baudrate
        self.stopbits = stopbits
        self.parity = parity
        self.timeout = timeout
        self.client = None

    def get_reserved_pins(self):
        """
        Zwraca listę pinów, które urządzenie chce zarezerwować.
        W przypadku Modbus nie rezerwuje żadnych pinów, więc zwraca pustą listę.
        """
        return []

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

    def read_holding_registers(self, slave_address, address, count):
        """
        Odczytuje rejestry "holding" z urządzenia Modbus.
        :param slave_address: Adres urządzenia Modbus.
        :param address: Początkowy adres rejestru.
        :param count: Liczba rejestrów do odczytu.
        :return: Lista wartości rejestrów.
        """
        response = self.client.read_holding_registers(address, count, slave=slave_address)
        if response.isError():
            raise ValueError(f"Modbus error: {response}")
        return response.registers

    def write_single_register(self, slave_address, address, value):
        """
        Zapisuje wartość do pojedynczego rejestru urządzenia Modbus.
        :param slave_address: Adres urządzenia Modbus.
        :param address: Adres rejestru.
        :param value: Wartość do zapisania.
        :return: Wynik operacji.
        """
        response = self.client.write_register(address, value, slave=slave_address)
        if response.isError():
            raise ValueError(f"Modbus error: {response}")
        return response

    def write_multiple_registers(self, slave_address, address, values):
        """
        Zapisuje wartości do wielu rejestrów urządzenia Modbus.
        :param slave_address: Adres urządzenia Modbus.
        :param address: Początkowy adres rejestru.
        :param values: Lista wartości do zapisania.
        :return: Wynik operacji.
        """
        response = self.client.write_registers(address, values, slave=slave_address)
        if response.isError():
            raise ValueError(f"Modbus error: {response}")
        return response
