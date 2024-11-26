
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
        self.port = port
        self.baudrate = baudrate
        self.stopbits = stopbits
        self.parity = parity
        self.timeout = timeout
        self.client = None

    def initialize(self):
        self.client = ModbusClient(port=self.port, baudrate=self.baudrate,
                                   stopbits=self.stopbits, parity=self.parity, timeout=self.timeout)
        if not self.client.connect():
            raise ConnectionError(f"Unable to connect to Modbus RTU server on port {self.port}.")
        print("Initializing Modbus TRU...")

    def release(self):
        if self.client:
            self.client.close()
        print("Releasing Modbus TRU...")

    def read_holding_registers(self, slave_address, address, count):
        response = self.client.read_holding_registers(address, count, slave=slave_address)
        if response.isError():
            raise ValueError(f"Modbus error: {response}")
        return response.registers

    def write_single_register(self, slave_address, address, value):
        response = self.client.write_register(address, value, slave=slave_address)
        if response.isError():
            raise ValueError(f"Modbus error: {response}")
        return response

    def write_multiple_registers(self, slave_address, address, values):
        response = self.client.write_registers(address, values, slave=slave_address)
        if response.isError():
            raise ValueError(f"Modbus error: {response}")
        return response
