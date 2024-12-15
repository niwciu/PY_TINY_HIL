# group2_runner.py
from core.test_group_factory import create_test_group
from .group2_tests import *

# Setup i teardown specyficzny dla tej grupy
# def setup_group():
#     TEST_INFO_MESSAGE("Setting up Group2")

# def teardown_group():
#     TEST_INFO_MESSAGE("Tearing down Group2")

setup_group = lambda: None
teardown_group = lambda: None

# Definicja testów
tests = [
    ("Test 1", sample_test_1),
    ("Test 2", sample_test_2),
    ("Test 3", sample_test_3)
]

# Tworzenie grupy testowej przy użyciu fabryki
group = create_test_group("Test_Group_2", setup_group, teardown_group, tests)
