# group2_runner.py
from core.test_group_factory import create_test_group
from .group2_tests import sample_test_1, sample_test_2, sample_test_3

# Setup i teardown specyficzny dla tej grupy
setup_group = lambda: None
teardown_group = lambda: None

# Definicja testów
tests = [
    ("Group2 Test 1", sample_test_1),
    ("Group2 Test 2", sample_test_2),
    ("Group2 Test 3", sample_test_3)
]

# Tworzenie grupy testowej przy użyciu fabryki
group = create_test_group("Group2 Group", setup_group, teardown_group, tests)