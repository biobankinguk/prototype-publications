from django.core.management.base import BaseCommand, CommandError

from django.conf import settings

from europepmc.models import Biobank, Publication, Annotation, Tag

import requests


class Command(BaseCommand):

    help = 'Import publications from EBI endpoint'

    def handle(self, *args, **options):

        for biobank in Biobank.objects.all():

            Publication.objects.filter(biobank=biobank).delete()
            publications = self.get_articles_from_pagination(biobank)
            print('{}, {}'.format(biobank.name, len(publications)))

            for publication in publications:
                pub_year = publication.get('pubYear', 0)
                title = publication.get('title', '')
                pid = publication.get('id', '')
                source = publication.get('source', '')
                doi = publication.get('doi', '')

                Publication.objects.get_or_create(
                    year=pub_year,
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
        print(endpoint.format(biobank))

        req = requests.get(endpoint.format(biobank))
        if req.status_code == 200:
            req_json = req.json()
            next_cursor = req_json.get('nextCursorMark', '')
            results = req_json.get('resultList', {}).get('result', [])
        else:
            next_cursor = ''
            results = []
        req.close()

        while next_cursor != '*' and next_cursor != '':
            req2 = requests.get(endpoint.format(biobank), params={'cursorMark': next_cursor})
            if req2.status_code == 200:
                req2_json = req2.json()
                next_cursor = req2_json.get('nextCursorMark', '')
                articles = req2_json.get('resultList', {}).get('result', [])
            else:
                next_cursor = ''
                articles = []
            req2.close()

            if not articles:
                break
            results.extend(articles)

        return results
