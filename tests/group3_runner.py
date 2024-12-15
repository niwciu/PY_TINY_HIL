from core.test_group_factory import create_test_group
from .group3_tests import *
from core.assertions import TEST_INFO_MESSAGE

# Setup i teardown specyficzny dla tej grupy
def setup_group():
    TEST_INFO_MESSAGE("Setting up Group3")

def teardown_group():
    TEST_INFO_MESSAGE("Tearing down Group3")

# setup_group = lambda: None
# teardown_group = lambda: None

# Definicja testów
tests = [
    ("Test 1", sample_test_1),
    ("Test 2", sample_test_2),
    ("Test 3", sample_test_3)
]

# Tworzenie grupy testowej przy użyciu fabryki
group = create_test_group("Test_Group_3", setup_group, teardown_group, tests)
