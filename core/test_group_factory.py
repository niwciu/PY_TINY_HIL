import os
import inspect
from core.test_framework import TestGroup, Test
from core.assertions import set_test_context, clear_test_context

def create_test_group(group_name, setup_func, teardown_func, tests):
    """
    Tworzy i zwraca obiekt TestGroup z przypisanymi testami, funkcjami setup i teardown.

    :param group_name: Nazwa grupy testowej.
    :param setup_func: Funkcja do uruchomienia przed testami.
    :param teardown_func: Funkcja do uruchomienia po testach.
    :param tests: Lista testów do przypisania do grupy, w formie [(test_name, test_function), ...]
    :return: Obiekt TestGroup z dodanymi testami.
    """
    # Ustal plik źródłowy dla testów
    if tests:
        _, first_test_func = tests[0]
        test_file = os.path.abspath(inspect.getsourcefile(first_test_func))
    else:
        test_file = None
        print(f"[WARNING] No tests provided for group '{group_name}'. test_file will be None.")

    group = TestGroup(group_name, test_file)

    # Opakowanie funkcji setup z dodaniem frameworka do kontekstu
    if setup_func:
        def wrapped_setup(framework):
            set_test_context(framework, group_name, "Global Setup")
            try:
                setup_func()
            finally:
                clear_test_context()
        group.set_setup(wrapped_setup)

    # Opakowanie funkcji teardown z dodaniem frameworka do kontekstu
    if teardown_func:
        def wrapped_teardown(framework):
            set_test_context(framework, group_name, "Global Teardown")
            try:
                teardown_func()
            finally:
                clear_test_context()
        group.set_teardown(wrapped_teardown)

    # Dodanie testów do grupy
    for test_name, test_func in tests:
        def wrapped_test(framework, group_name=group_name, test_name=test_name, test_func=test_func):
            set_test_context(framework, group_name, test_name)
            try:
                test_func(framework, group_name, test_name)
            finally:
                clear_test_context()

        group.add_test(Test(test_name, wrapped_test, test_func))

    return group
