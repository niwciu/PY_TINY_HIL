from core.test_group_factory import create_test_group
from .modbus_communication_tests import modbus_read_test

# Funkcje setup i teardown specyficzne dla grupy
def setup_group():
    print("Setting up Modbus Communication Tests")

def teardown_group():
    print("Tearing down Modbus Communication Tests")

# Definicja testów
tests = [
    ("Read Holding Register Test", modbus_read_test)
]

# Tworzenie grupy testowej przy użyciu fabryki
modbus_communication_group = create_test_group("Modbus Communication Tests", setup_group, teardown_group, tests)
