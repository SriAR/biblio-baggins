import subprocess
from typing import List

class Rofi:

    def __init__(self, dmenu = True, theme = 'pdfs', insensitive = True, sort = False, multiselect = False, index = False):

        self.dmenu = dmenu
        self.theme = theme
        self.insensitive = insensitive
        self.sort = sort
        self.multiselect = multiselect
        self.index = index

    def menu(self, options: List[str], prompt = "Enter Textka"):
        """
        Displays a rofi menu with the given options and prompt.

        Args:
            prompt (str, optional): The prompt to display at the top of the rofi menu. Defaults to "Enter Textka".
            options (List[str]): A list of strings representing the options to display in the rofi menu.

        Returns:
            str or None: The selected option if an option is selected, None if the user cancels the menu.
        """
        args = ['rofi']

        if self.dmenu:
            args.append('-dmenu')
        if self.theme:
            args += ['-theme', self.theme]
        if self.insensitive:
            args.append('-i')
        if self.sort:
            args.append('-sort')
        if self.multiselect:
            args.append('-multi-select')
        if self.index:
            args += ['-format', 'i']

        args += ['-p', prompt]

        proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, _ = proc.communicate(input='\n'.join(options).encode())

        if proc.returncode == 0:
            return stdout.decode().strip()
        else:
            return None
