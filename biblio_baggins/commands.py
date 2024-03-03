import pyperclip
from .dblp import DBLP
from .rofi import Rofi
from .choosepapers import ChoosePapers
from .notify import evrart
import json

def paperadd():
    dblp_instance = DBLP()
    paper_chooser = ChoosePapers()

    #  rofi_instance = Rofi()
    #  query_string = rofi_instance.menu([], prompt="Enter Query")

    query_string = pyperclip.paste()
    evrart.say("My boys are on it", f"They are leaving no stone unturned searching for\n {query_string},\n Harry!")

    search_results = dblp_instance.search(query_string)

    paper_chooser.populate(search_results)

    paper_for_bib = paper_chooser.bibselect()
    paper_for_pdf = paper_chooser.pdfselect()

    if paper_for_bib is not None:
        paper_for_bib.get_bibtex()
    else:
        print('nobib')

    if paper_for_pdf is not None:
        paper_for_pdf.get_pdf()
    else:
        print('nopdf')
