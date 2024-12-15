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
    group = TestGroup(group_name)
    group.set_setup(setup_func)
    group.set_teardown(teardown_func)

    for test_name, test_func in tests:
        # Opakowanie funkcji testowej, przechowując bieżące wartości zmiennych jako domyślne argumenty
        def wrapped_test(framework, group_name=group_name, test_name=test_name, test_func=test_func):
            """
            Opakowanie funkcji testowej w celu przekazania brakujących argumentów i ustawienia kontekstu.
            """
            # Ustawiamy globalny kontekst dla asercji
            set_test_context(framework, group_name, test_name)
            try:
                # Wywołujemy rzeczywistą funkcję testową z wymaganymi argumentami
                test_func(framework, group_name, test_name)
            finally:
                # Czyszczenie kontekstu po wykonaniu testu
                clear_test_context()

        # Dodanie opakowanego testu do grupy
        group.add_test(Test(test_name, wrapped_test))
    
    return group
