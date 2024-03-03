import requests

class PdfDownloader:
    def __init__(self):
        self.arxiv_url = 'https://arxiv.org/pdf/'
        self.scihub_url = 'https://sci-hub.se/'

    #  def download_pdf(self, bibentry):
    #      if 'arxiv' in bibentry.fields.get('eprint', '').lower():
    #          return self._download_arxiv_pdf(bibentry)
    #      elif bibentry.fields.get('doi'):
    #          return self._download_doi_pdf(bibentry)
    #      else:
    #          raise ValueError('Bibentry does not contain a valid arXiv ID or DOI.')

    def download_from_arxiv(self, arxiv_id):
        #  arxiv_id = bibentry.fields.get('eprint')
        #  if not arxiv_id:
        #      return None

        url = self.arxiv_url + arxiv_id + '.pdf'
        return self._download_pdf(url)

    def download_from_scihub(self, bibentry):
        doi = bibentry.fields.get('doi')
        if not doi:
            return None

        url = self.scihub_url + doi
        response = requests.get(url)
        if response.status_code != 200:
            return None

        # Sci-Hub returns a page with a hidden iframe that contains the PDF URL
        iframe_url = self._get_scihub_iframe_url(response.text)
        if not iframe_url:
            return None

        return self._download_pdf(iframe_url)

    def _download_pdf(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            return None

        return response.content

    def _get_scihub_iframe_url(self, html):
        start = html.find('<iframe src="')
        if start == -1:
            return None

        start += len('<iframe src="')
        end = html.find('"', start)
        if end == -1:
            return None

        return html[start:end]
