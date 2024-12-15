import os
import re
from termcolor import colored


class Logger:
    def __init__(self, log_file=None):
        """
        Inicjalizuje logger.
        :param log_file: Opcjonalna ścieżka do pliku logów.
        """
        self.log_file = log_file
        self.log_buffer = ""  # Bufor dla logów plikowych
        self._file_initialized = False  # Flaga do jednorazowego czyszczenia pliku logów

        # Wyczyść plik logów, jeśli istnieje
        if self.log_file:
            self._initialize_log_file()

    def log(self, message, to_console=True, to_log_file=False):
        """
        Loguje wiadomość zgodnie z ustawionymi włącznikami.
        :param message: Wiadomość do zalogowania.
        :param to_console: Czy wyświetlić wiadomość w konsoli.
        :param to_log_file: Czy zapisać wiadomość do pliku logów.
        """
        # Logowanie do konsoli
        if to_console:
            self._log_to_console(message)

        # Logowanie do pliku
        if to_log_file and self.log_file:
            self._log_to_file(message)

    def _log_to_console(self, message):
        """
        Logowanie wiadomości do konsoli z kolorowaniem.
        """
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

    def _log_to_file(self, message):
        """
        Logowanie wiadomości do pliku.
        """
        if not self._file_initialized:
            self._initialize_log_file()

        with open(self.log_file, 'a') as f:
            f.write(message + "\n")

    def _initialize_log_file(self):
        """
        Czyści zawartość pliku logów przy pierwszym zapisie.
        """
        with open(self.log_file, 'w') as f:
            f.write("")  # Tworzenie pustego pliku logów
        self._file_initialized = True  # Flaga ustawiona, aby plik był czyszczony tylko raz

    def flush_log(self):
        """
        Zapisuje bufor logów do pliku i czyści bufor.
        """
        if not self.log_file:
            return

        with open(self.log_file, 'a') as log_file:
            log_file.write(self.log_buffer)
        self.log_buffer = ""
