import os
import sys
import importlib
from core.test_framework import TestFramework, TestGroup
from core.logger import Logger
from core.peripheral_manager import PeripheralManager
from core.protocols import ModbusTRU
from core.RPiPeripherals import RPiGPIO, RPiPWM, RPiUART, RPiI2C, RPiSPI
from core.peripheral_config_loader import load_peripheral_configuration

def load_test_groups(test_directory):
    """
    Loads test groups from the specified directory.
    :param test_directory: Directory containing test group runner files.
    :return: List of TestGroup objects.
    """
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
    # Parse command-line arguments
    log_file = None
    html_file = None
    if len(sys.argv) > 2:
        if '--log' in sys.argv:
            log_index = sys.argv.index('--log')
            log_file = sys.argv[log_index + 1] if log_index + 1 < len(sys.argv) else None
        if '--html' in sys.argv:
            html_index = sys.argv.index('--html')
            html_file = sys.argv[html_index + 1] if html_index + 1 < len(sys.argv) else None

    # Setup logger
    logger = Logger(log_file=log_file, html_file=html_file)

    # Create PeripheralManager instance
    peripheral_manager = PeripheralManager(devices={}, logger=logger)
    peripheral_manager.devices = load_peripheral_configuration()

    # Load test groups dynamically
    test_directory = os.path.join(os.path.dirname(__file__), 'tests')
    test_groups = load_test_groups(test_directory)
    print(f"Discovered test groups: {test_groups}")

    # Create TestFramework instance
    test_framework = TestFramework(peripheral_manager, logger)

    # Add test groups to the framework
    for group in test_groups:
        test_framework.add_test_group(group)

    try:
        # Run all tests
        test_framework.run_all_tests()

        # Generate HTML report with test groups
        if html_file:
            logger.generate_html_report(test_groups=test_groups)
    except SystemExit as e:
        # Handle test framework exit
        if html_file:
            logger.generate_html_report(test_groups=test_groups)
        logger.log(f"[INFO] Test execution stopped with exit code {e.code}.")
        sys.exit(e.code)

if __name__ == "__main__":
    main()
