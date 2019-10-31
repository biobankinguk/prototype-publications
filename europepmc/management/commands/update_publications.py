from django.core.management.base import BaseCommand, CommandError

from europepmc.models import Biobank, Publication, Annotation, Tag

import pyodbc
import requests


class Command(BaseCommand):

    help = 'Import publications from EBI endpoint'

    def handle(self, *args, **options):

        endpoint = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=ACK_FUND:"{}"&format=json'

        for biobank in Biobank.objects.all():

            r = requests.get(endpoint.format(biobank))

            for publication in r.json()['resultList']['result']:
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
