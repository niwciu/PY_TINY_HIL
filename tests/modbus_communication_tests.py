
# modbus_communication_tests.py
from core.protocols import ModbusTRU

def modbus_read_test(framework, group_name, test_name):
    try:
        # Pobranie zasobu ModbusTRU z menedżera
        modbus_peripheral = framework.peripheral_manager.get_device("protocols", "ModbusTRU")

        # Korzystanie z zasobu
        registers = modbus_peripheral.read_holding_registers(slave_address=0x01, address=0x00, count=1)

        # Sprawdzenie wartości
        if registers[0] == 0x5A5A:
            framework.report_test_result(group_name, test_name, True)
        else:
            framework.report_test_result(group_name, test_name, False, f"Expected value 0x5A5A, got {registers[0]:#06x}")
    except Exception as e:
        framework.report_test_result(group_name, test_name, False, str(e))
