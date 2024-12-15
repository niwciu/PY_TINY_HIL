# group2_tests.py
from core.test_framework import Test
from core.assertions import *

def sample_test_1(framework, group_name, test_name):
    TEST_INFO_MESSAGE("TEST")

def sample_test_2(framework, group_name, test_name):
    TEST_ASSERT_EQUAL(4,51)

def sample_test_3(framework, group_name, test_name):
    TEST_ASSERT_EQUAL(4,4)
