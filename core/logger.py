import re
from termcolor import colored


class Logger:
    def __init__(self, log_file=None):
        """
        Inicjalizuje logger.
        :param log_file: Opcjonalna ścieżka do pliku logów.
        """
        self.log_file = log_file
        self.log_buffer = ""

    def log(self, message, to_console=True):
        """
        Loguje wiadomość do konsoli i/lub do pliku logów.
        :param message: Wiadomość do zalogowania.
        :param to_console: Czy wyświetlić wiadomość w konsoli.
        """
        if to_console:
            # Kolorowanie komunikatów [PASS], [FAIL], [INFO], [WARNING], [ERROR]
            message_with_color = re.sub(
                r'\[(PASS|FAIL|INFO|WARNING|ERROR)\]',
                lambda m: '[' + colored(
                    m.group(1),
                    'green' if m.group(1) == 'PASS' else
                    'red' if m.group(1) in ('FAIL', 'ERROR') else
                    'blue' if m.group(1) == 'INFO' else
                    'yellow'
                ) + ']',
                message
            )
            print(message_with_color)

        # Zapisywanie wiadomości do bufora i opcjonalnie do pliku
        self.log_buffer += message + "\n"
        if self.log_file:
            with open(self.log_file, 'w') as f:
                f.write(self.log_buffer)

    def flush_log(self):
        """
        Zapisuje bufor logów do pliku i czyści bufor.
        """
        if not self.log_file:
            return

        with open(self.log_file, 'a') as log_file:
            log_file.write(self.log_buffer)
        self.log_buffer = ""
