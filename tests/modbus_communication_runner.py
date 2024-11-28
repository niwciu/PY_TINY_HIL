from core.test_group_factory import create_test_group
from .modbus_communication_tests import modbus_read_test
from core.logger import Logger

# Funkcje setup i teardown specyficzne dla grupy
def setup_group():
    print()

def teardown_group():
    print()


# Definicja testów
tests = [
    ("Read Holding Register Test", modbus_read_test)
]

# Tworzenie grupy testowej przy użyciu fabryki
modbus_communication_group = create_test_group("Modbus Communication Tests", setup_group, teardown_group, tests)
