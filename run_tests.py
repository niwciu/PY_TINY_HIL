import sys
import os
import importlib
from core.test_framework import TestFramework, TestGroup
from core.logger import Logger
from core.peripheral_manager import PeripheralManager
from core.protocols import ModbusTRU
from core.RPiPeripherals import RPiGPIO, RPiPWM, RPiUART, RPiI2C, RPiSPI
import RPi.GPIO as GPIO

def load_test_groups(test_directory):
    test_groups = []
    for file_name in os.listdir(test_directory):
        if file_name.endswith("_runner.py"):  # Load only runner files
            module_name = f"tests.{file_name[:-3]}"  # Remove the .py extension
            module = importlib.import_module(module_name)
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, TestGroup):
                    test_groups.append(attr)
    return test_groups

def main():
    # Setup logger
    logger = Logger()

    if len(sys.argv) > 2 and sys.argv[1] == '--log':
        logger.log_file = sys.argv[2]

    # Create PeripheralManager instance
    peripheral_manager = PeripheralManager(devices={}, logger=logger)

    # Define peripherals and protocols
    pwm = RPiPWM(pin=12, frequency=1000)  # PWM na GPIO12
    uart = RPiUART(port='/dev/serial0', baudrate=9600)  # UART
    i2c = RPiI2C(bus=1)  # I2C
    spi = RPiSPI(bus=0, device=0)  # SPI

    # GPIO configuration
    gpio = RPiGPIO({
        17: {'mode': GPIO.OUT, 'initial': GPIO.LOW},
        18: {'mode': GPIO.IN}
    })

    # Add devices to the manager
    devices = {
        "protocols": [ModbusTRU()],
        "peripherals": [gpio, pwm, uart, i2c, spi]
    }
    peripheral_manager.devices = devices

    # Create TestFramework instance
    test_framework = TestFramework(peripheral_manager, logger)

    # Load and add test groups automatically
    test_directory = os.path.join(os.path.dirname(__file__), 'tests')
    test_groups = load_test_groups(test_directory)

    for group in test_groups:
        test_framework.add_test_group(group)

    try:
        # Run all tests (TestFramework should handle initialization itself)
        test_framework.run_all_tests()
    except SystemExit as e:
        # If tests fail or are stopped
        logger.log(f"[WARNING] Test execution stopped with exit code {e.code}.")
        sys.exit(e.code)

if __name__ == "__main__":
    main()
