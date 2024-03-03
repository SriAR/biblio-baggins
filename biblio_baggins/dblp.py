import requests
import webbrowser
from typing import List
from .logger import logger
from .helpers import pp
from .notify import evrart
from .pdf import PdfDownloader
import bibtexparser
import pyperclip


class DBLPEntryNotFoundError(Exception):
    def __init__(self, query):
        self.notify_user(query)

    def notify_user(self, query):
        evrart.say(
            title=f"You lost your {query}?",
            message=f"My workers could not find your {query}, Harry.",
        )

        super().__init__(f"No DBLP entries found for query: {query}")


class DBLPEntry:
    def __init__(
        self,
        info,
        key: str,
        title: str,
        authors: List[str],
        year: str,
        url: str,
        venue: str = None,
        doi: str = None,
        ee: str = None,
        openaccess: bool = False,
    ):
        self.info = info
        self.key = key
        self.title = title
        self.authors = authors
        self.year = year
        self.url = url
        self.venue = venue
        self.doi = doi
        self.ee = ee
        self.openaccess = openaccess

    @classmethod
    def from_hit(cls, hit: dict):
        info = hit["info"]
        key = hit["info"]["key"]
        title = hit["info"]["title"]
        authors = []
        if "authors" in hit["info"]:
            authors_dict = hit["info"]["authors"]["author"]
            if isinstance(authors_dict, dict):
                authors_dict = [authors_dict]
            for author in authors_dict:
                authors.append(author["text"])
        year = hit["info"]["year"]
        url = hit["info"]["url"] if "url" in hit["info"] else None
        venue = hit["info"]["venue"] if "venue" in hit["info"] else None
        doi = hit["info"]["doi"] if "doi" in hit["info"] else None
        ee = hit["info"]["ee"] if "ee" in hit["info"] else None
        openaccess = True if hit["info"]["access"] == "open" else False
        return cls(info, key, title, authors, year, url, venue, doi, ee, openaccess)

    def get_bibtex(self):
        url = f"https://dblp.org/rec/{self.key}.bib"
        response = requests.get(url)
        response.raise_for_status()
        #  print(response.content)
        #  return bibtexparser.parse_string(response.content).entries[0]
        self.save_bibtex(response.content)

    def save_bibtex(self, bibtex):
        filename = "/tmp/a.bib"

        with open(filename, "wb") as file:
            file.write(bibtex)

        evrart.say(
            title="Found your bibtex",
            message="My workers have found your bibtex file, Harry",
        )

    def get_pdf(self):
        #  print(pp(self.info))
        if self.info["venue"] == "CoRR":
            arxiv_id = self.info["volume"].split("/")[1]

            dler = PdfDownloader()
            pdf = dler.download_from_arxiv(arxiv_id)

            filename = "/tmp/a.pdf"

            with open(filename, "wb") as file:
                file.write(pdf)

            evrart.say(
                title="Found your pdf",
                message="My workers have found your pdf file, Harry",
            )

        elif self.openaccess:
            webbrowser.open(self.ee)

        else:
            webbrowser.open(self.ee)
            webbrowser.open(
                "https://scholar.google.com/scholar?q="
                + pyperclip.paste().replace(" ", "+")
            )

    def __repr__(self):
        repr_str = f"\n{self.title} ({self.year})"
        if self.authors:
            repr_str += f" by {', '.join(self.authors)}"
        if self.venue:
            repr_str += f"\nVenue: {self.venue}"
        if self.doi:
            repr_str += f"\nDOI: {self.doi}"
        if self.ee:
            repr_str += f"\nEE: {self.ee}"
        return repr_str + "\n"


class DBLP:
    def __init__(self):
        self.base_url = "https://dblp.org/search/publ/api"
        self.base_url = "https://dblp.uni-trier.de/search/publ/api"

    def search(self, query: str) -> List[DBLPEntry]:
        formatted_query = query.replace(" ", "+")
        logger.info(f"Formatted DBLP Query: {formatted_query}")
        params = {"q": formatted_query, "format": "json"}

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            logger.info(f"DBLP Query Response JSON:\n {pp(data)}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request to DBLP failed: {e}")
            raise e

        if int(data["result"]["hits"]["@total"]) == 0:
            raise DBLPEntryNotFoundError(query)

        return self.parse_json(data)

    def parse_json(self, data):
        hits = data["result"]["hits"]["hit"]
        if isinstance(hits, dict):
            hits = [hits]

        entries = [DBLPEntry.from_hit(hit) for hit in hits]
        #  logger.info(f"Created the following entries:\n {entries}")
        return entries
