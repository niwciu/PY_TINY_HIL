import sys
import os
import importlib
from core.test_framework import TestFramework, TestGroup
from core.logger import Logger
from core.peripheral_manager import PeripheralManager
from core.protocols import ModbusTRU
from core.RPiPeripherals import RPiGPIO, RPiPWM, RPiUART, RPiI2C, RPiSPI
from core.peripheral_config_loader import load_peripheral_configuration
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
    log_file = None
    html_file = None
    if len(sys.argv) > 1:
        if '--log' in sys.argv:
            log_index = sys.argv.index('--log')
            log_file = sys.argv[log_index + 1] if log_index + 1 < len(sys.argv) else None
        if '--html' in sys.argv:
            html_index = sys.argv.index('--html')
            html_file = sys.argv[html_index + 1] if html_index + 1 < len(sys.argv) else None

    logger = Logger(log_file=log_file, html_file=html_file)

    # Create PeripheralManager instance
    peripheral_manager = PeripheralManager(devices={}, logger=logger)
    peripheral_manager.devices = load_peripheral_configuration()
    print(peripheral_manager.devices)

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

        # Generate HTML report if requested
        if html_file:
            logger.generate_html_report()

    except SystemExit as e:
        # If tests fail or are stopped
        logger.log(f"[INFO] Test execution stopped with exit code {e.code}.")
        sys.exit(e.code)

if __name__ == "__main__":
    main()
