#assertion.py
_current_context = {}  # Globalny słownik do przechowywania kontekstu

def set_test_context(framework, group_name, test_name):
    """
    Ustawia globalny kontekst testu.
    :param framework: Instancja frameworku testowego.
    :param group_name: Nazwa grupy testowej.
    :param test_name: Nazwa testu.
    """
    _current_context["framework"] = framework
    _current_context["group_name"] = group_name
    _current_context["test_name"] = test_name


def clear_test_context():
    """
    Czyści globalny kontekst testu.
    """
    _current_context.clear()

def TEST_FAIL_MESSAGE(message, context=None):
    """
    Asercja raportująca niepowodzenie testu z podanym komunikatem.
    Jeśli kontekst (context) jest dostępny, raportuje wynik przez framework.
    Jeśli brak kontekstu, przechowuje symbol do późniejszego wykonania.
    """
    if context or _current_context:
        # Jeśli mamy kontekst (z argumentów lub globalny), wykonaj asercję
        framework = (context or _current_context).get("framework")
        group_name = (context or _current_context).get("group_name")
        test_name = (context or _current_context).get("test_name")
        framework.report_test_result(
            group_name,
            test_name,
            False,
            message
        )
    else:
        # Jeśli brak kontekstu, przechowaj symbol do późniejszego wykonania
        return ("TEST_FAIL_MESSAGE", message)


def TEST_INFO_MESSAGE(message, context=None):
    """
    Loguje wiadomość informacyjną z podanym komunikatem.
    Jeśli kontekst (context) jest dostępny, używa frameworka do logowania.
    Jeśli brak kontekstu, przechowuje symbol do późniejszego wykonania.
    """
    if context or _current_context:
        # Jeśli mamy kontekst, wykonaj logowanie przez framework
        framework = (context or _current_context).get("framework")
        group_name = (context or _current_context).get("group_name")
        test_name = (context or _current_context).get("test_name")
        framework.report_test_info(group_name, test_name, message)
    else:
        # Jeśli brak kontekstu, przechowaj symbol do późniejszego wykonania
        return ("TEST_INFO_MESSAGE", message)

    
def TEST_ASSERT_EQUAL(expected, actual, context=None):
    """
    Symboliczna asercja sprawdzająca równość.
    :param actual: Aktualna wartość.
    :param expected: Oczekiwana wartość.
    :param context: (Opcjonalny) Słownik zawierający framework, grupę i nazwę testu.
    """
    if context or _current_context:
        # Jeśli mamy kontekst (z argumentów lub globalny), wykonaj asercję
        framework = (context or _current_context).get("framework")
        group_name = (context or _current_context).get("group_name")
        test_name = (context or _current_context).get("test_name")
        if actual != expected:
            framework.report_test_result(
                group_name,
                test_name,
                False,
                f"Assertion failed! Expected value = {expected}, actual value = {actual} "
            )
        else:
            framework.report_test_result(group_name, test_name, True)
    else:
        # Jeśli brak kontekstu, przechowaj symbol do późniejszego wykonania
        return ("TEST_ASSERT_EQUAL", actual, expected)


def TEST_ASSERT_TRUE(condition, context=None):
    """
    Symboliczna asercja sprawdzająca, czy warunek jest prawdziwy.
    :param condition: Warunek do sprawdzenia.
    :param context: (Opcjonalny) Słownik zawierający framework, grupę i nazwę testu.
    """
    if context or _current_context:
        framework = (context or _current_context).get("framework")
        group_name = (context or _current_context).get("group_name")
        test_name = (context or _current_context).get("test_name")
        if not condition:
            framework.report_test_result(
                group_name,
                test_name,
                False,
                f"Assertion failed: condition is not true"
            )
        else:
            framework.report_test_result(group_name, test_name, True)
    else:
        return ("TEST_ASSERT_TRUE", condition)


def TEST_ASSERT_IN(item, collection, context=None):
    """
    Symboliczna asercja sprawdzająca, czy element znajduje się w kolekcji.
    :param item: Element do sprawdzenia.
    :param collection: Kolekcja, w której szukamy elementu.
    :param context: (Opcjonalny) Słownik zawierający framework, grupę i nazwę testu.
    """
    if context or _current_context:
        framework = (context or _current_context).get("framework")
        group_name = (context or _current_context).get("group_name")
        test_name = (context or _current_context).get("test_name")
        if item not in collection:
            framework.report_test_result(
                group_name,
                test_name,
                False,
                f"Assertion failed: {item} not in {collection}"
            )
        else:
            framework.report_test_result(group_name, test_name, True)
    else:
        return ("TEST_ASSERT_IN", item, collection)
