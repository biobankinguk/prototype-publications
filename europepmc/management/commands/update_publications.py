from django.core.management.base import BaseCommand, CommandError

from europepmc.models import Biobank, Publication, Annotation, Tag

# import pyodbc
import requests


class Command(BaseCommand):

    help = 'Import publications from EBI endpoint'

    # def handle(self, *args, **options):
    #
    #     endpoint = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=ACK_FUND:"{}"&format=json'
    #
    #     for biobank in Biobank.objects.all():
    #
    #         r = requests.get(endpoint.format(biobank))
    #
    #         for publication in r.json()['resultList']['result']:
    #             pubYear = publication['pubYear']
    #             title = publication['title']
    #             pid = publication['id']
    #             source = publication['source']
    #
    #             try:
    #                 doi = publication['doi']
    #             except KeyError as e:
    #                 doi = ''
    #
    #             Publication.objects.get_or_create(
    #                 year=pubYear,
    #                 title=title,
    #                 biobank=biobank,
    #                 pid=pid,
    #                 source=source,
    #                 doi=doi,
    #             )

    def handle(self, *args, **options):

        # endpoint = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=ACK_FUND:"{}"&format=json'

        for biobank in Biobank.objects.all():

            publications = self.get_articles_from_pagination(biobank)

            for publication in publications:
                pubYear = publication['pubYear']
                title = publication['title']
                pid = publication['id']
                source = publication['source']

                try:
                    doi = publication['doi']
                except KeyError as e:
                    doi = ''

                Publication.objects.get_or_create(
                    year=pubYear,
                    title=title,
                    biobank=biobank,
                    pid=pid,
                    source=source,
                    doi=doi,
                )

    def get_articles_from_pagination(self, biobank: str):
        """
        iterate over a paginated request to get all the articles
        :return:
        """

        endpoint = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=ACK_FUND:"{}"&format=json'

        req = requests.get(endpoint.format(biobank))
        req_json = req.json()
        req.close()

        next_cursor = req_json.get('nextCursorMark', '')
        # hit_count = req_json.get('hitCount', 0)
        results = req_json.get('resultList', {}).get('result', [])
        print(req.url)

        while next_cursor != '*' and next_cursor != '':
            req2 = requests.get(endpoint, params={'cursorMark': next_cursor})
            req2_json = req2.json()
            req2.close()

            next_cursor = req2_json.get('nextCursorMark', '')
            articles = req2_json.get('resultList', {}).get('result', [])
            if not articles:
                break
            results.extend(articles)

        return results
