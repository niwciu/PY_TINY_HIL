# PY_MICRO_HIL

PY_MICRO_HIL is a flexible and modular Hardware-in-the-Loop (HIL) testing framework designed for validating and verifying embedded systems. This framework supports the integration of hardware peripherals and communication protocols such as Modbus for comprehensive testing.

## Features

- **Peripheral Management:** Configure and control hardware peripherals with ease using YAML configuration files.
- **Protocol Support:** Includes built-in support for Modbus communication.
- **Test Framework:** Modular and scalable testing framework for defining and running test cases.
- **Logging:** Enhanced logging with colored output for better readability.
- **Extensibility:** Easily extendable to support additional peripherals and protocols.

## Project Structure

```
PY_MICRO_HIL/
├── core/                   # Core functionality
│   ├── RPiPeripherals.py   # Raspberry Pi peripheral management
│   ├── assertions.py       # Assertion functions for test validations
│   ├── logger.py           # Logging utility
│   ├── peripheral_config_loader.py  # YAML configuration loader
│   ├── peripheral_manager.py        # Peripheral manager
│   ├── protocols.py        # Communication protocol handlers
│   ├── test_framework.py   # Main testing framework
│   ├── test_group_factory.py  # Test group management
│   └── __init__.py         # Module initializer
├── tests/                  # Test definitions
│   ├── group2_runner.py    # Runner for group 2 tests
│   ├── group2_tests.py     # Test cases for group 2
│   ├── group3_runner.py    # Runner for group 3 tests
│   ├── group3_tests.py     # Test cases for group 3
│   ├── modbus_communication_runner.py  # Modbus tests runner
│   ├── modbus_communication_tests.py   # Modbus test cases
│   └── __init__.py         # Module initializer
├── peripherals_config.yaml # Peripheral configuration file
├── requirements.txt        # Python dependencies
├── run_tests.py            # Entry point for running tests
├── dependencies.txt        # Additional dependencies
└── .gitignore              # Git ignored files
```

## Requirements

- Python 3.8 or later
- Hardware peripherals for embedded systems (optional for actual hardware testing)
- Required Python packages (see `requirements.txt`)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd PY_MICRO_HIL
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your peripherals:
   - Edit the `peripherals_config.yaml` file to match your hardware setup.

## Usage

### Running Tests
To run all tests, execute:
```bash
python run_tests.py
```

### Adding New Tests
1. Create a new test group in the `tests/` directory.
2. Define your test cases in a Python file (e.g., `groupX_tests.py`).
3. Create a runner script for your new group (e.g., `groupX_runner.py`).
4. Use the `TestFramework` and `TestGroup` classes to structure your tests.

### Peripheral Configuration
Edit the `peripherals_config.yaml` file to define your hardware peripherals, communication protocols, and any additional parameters. Example:
```yaml
peripherals:
  - name: sensor1
    type: gpio
    pin: 17
  - name: modbus_device
    type: modbus
    address: 0x01
```

## Contribution Guidelines

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes with descriptive messages.
4. Submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Support

If you encounter any issues or have questions, feel free to open an issue or contact the maintainers.
