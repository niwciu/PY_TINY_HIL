# logger.py
import re
from termcolor import colored

class Logger:
    def __init__(self, log_file=None):
        self.log_file = log_file
        self.log_buffer = ""

    def log(self, message, to_console=True):
        if to_console:
            message_with_color = re.sub(r'\[(PASS|FAIL)\]', lambda m: '[' + colored(m.group(1), 'green' if m.group(1) == 'PASS' else 'red') + ']', message)
            print(message_with_color)

        if not to_console or not self.log_file:
            self.log_buffer += message + "\n"
            if self.log_file:
                with open(self.log_file, 'w') as f:
                    f.write(self.log_buffer)

    def flush_log(self):
        if not self.log_file:
            return

        with open(self.log_file, 'a') as log_file:
            log_file.write(self.log_buffer)
        self.log_buffer = ""

# To przeniesiono z Core      
# class Logger:
#     def __init__(self, log_file=None):
#         self.log_file = log_file
#         self.log_buffer = ""

#     def log(self, message, to_console=True):
#         if to_console:
#             message_with_color = re.sub(r'\[(PASS|FAIL)\]', lambda m: '[' + colored(m.group(1), 'green' if m.group(1) == 'PASS' else 'red') + ']', message)
#             print(message_with_color)

#         if not to_console or not self.log_file:
#             self.log_buffer += message + "\n"
#             if self.log_file:
#                 with open(self.log_file, 'w') as f:
#                     f.write(self.log_buffer)