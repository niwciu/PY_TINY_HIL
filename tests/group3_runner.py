# group3_runner.py
from core.test_group_factory import create_test_group
from .group3_tests import *

# Setup i teardown specyficzny dla tej grupy
# Funkcje setup i teardown specyficzne dla grupy
# def setup_group():

# def teardown_group():

setup_group = lambda: None
teardown_group = lambda: None

# Definicja testów
tests = [
    ("Group3 Test 1", sample_test_1),
    ("Group3 Test 2", sample_test_2),
    ("Group3 Test 3", sample_test_3)
]

# Tworzenie grupy testowej przy użyciu fabryki
group = create_test_group("Group3 Group", setup_group, teardown_group, tests)
