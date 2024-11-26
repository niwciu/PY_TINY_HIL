# test_group_factory.py
from core.test_framework import TestGroup, Test

def create_test_group(group_name, setup_func, teardown_func, tests):
    """
    Tworzy i zwraca obiekt TestGroup z przypisanymi testami, funkcjami setup i teardown.

    :param group_name: Nazwa grupy testowej.
    :param setup_func: Funkcja do uruchomienia przed testami.
    :param teardown_func: Funkcja do uruchomienia po testach.
    :param tests: Lista testów do przypisania do grupy, w formie [(test_name, test_function), ...]
    :return: Obiekt TestGroup z dodanymi testami.
    """
    group = TestGroup(group_name)
    group.set_setup(setup_func)
    group.set_teardown(teardown_func)
    
    for test_name, test_func in tests:
        group.add_test(Test(test_name, test_func))
    
    return group
