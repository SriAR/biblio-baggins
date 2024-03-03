from typing import List
from .rofi import Rofi
from .dblp import DBLPEntry

class ChoosePapers:
    def __init__(self, entries: List[DBLPEntry] = []):
        self.entries = entries
        self.rofi = Rofi(index=True)

    def populate(self, entries):
        self.entries += entries

    def bibselect(self):
        return self.select()

    def pdfselect(self):
        return self.select()

    def select(self):
        options = [f"{'+' if entry.openaccess else '-'} - {entry.venue}{entry.year} - {', '.join(entry.authors[:3])} - {entry.title}" for entry in self.entries]
        #  selected_indices = self.rofi.menu(options, prompt="Select Papers")
        selected_index = self.rofi.menu(options, prompt="Select Papers")

        if selected_index:
            return self.entries[int(selected_index)]
        else:
            return None

        #  if selected_indices:
        #      selected_indices = selected_indices.split("\n")
        #      return [self.entries[int(i)] for i in selected_indices]
        #  else:
        #      return []
