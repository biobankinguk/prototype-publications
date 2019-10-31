from django.core.management.base import BaseCommand, CommandError

from europepmc.models import Biobank, Publication, Annotation, Tag

import pyodbc
import requests


class Command(BaseCommand):

    help = 'Import publications from EBI endpoint'

    def handle(self, *args, **options):

        server = 'UiWdtSQL09.nottingham.ac.uk'
        database = 'biobankinguk'
        username = 'WPConnectBioBank'
        password = 'u9aH6rBFuf040Ofg8mxyEXjfp'
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = cnxn.cursor()

        endpoint = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=ACK_FUND:"{}"&format=json'
        articles_endpoint = 'https://www.ebi.ac.uk/europepmc/annotations_api/annotationsByArticleIds?articleIds={}:{}&format=JSON'

        biobanks = {}
        publications = {}

        # tsql = "SELECT name FROM organisations WHERE name='Northern Ireland Biobank (NIB)'"
        # # tsql = "SELECT name FROM organisations"
        # with cursor.execute(tsql):
        #     row = cursor.fetchone()
        #     while row:
        #         biobanks[row[0]] = {}

        #         Biobank.objects.get_or_create(
        #             name=row[0]
        #         )

        #         row = cursor.fetchone()
                
        # for biobank in Biobank.objects.all():

        #     r = requests.get(endpoint.format(biobank))

        #     publications[biobank] = {}
        #     publications[biobank]['hitCount'] = r.json()['hitCount']
        #     publications[biobank]['publications'] = {}
            
        #     for publication in r.json()['resultList']['result']:
        #         pubYear = publication['pubYear']
        #         title = publication['title']
        #         pid = publication['id']
        #         source = publication['source']

        #         Publication.objects.get_or_create(
        #             year=pubYear,
        #             title=title,
        #             biobank=biobank,
        #             pid=pid,
        #             source=source,
        #         )

        # for publication in Publication.objects.all():
        for publication in Publication.objects.all()[:5]:

            r_articles = requests.get(articles_endpoint.format(publication.source, publication.pid))

            for annotation in r_articles.json()[0]['annotations']:

                print(annotation['prefix'])
                print(annotation['exact'])
                print(annotation['id'])
                print(annotation['type'])
                print(annotation['section'])
                print(annotation['provider'])

                annotation_obj, created = Annotation.objects.get_or_create(
                    publication=publication,
                    exact=annotation['exact'],
                    aid=annotation['id'],
                    atype=annotation['type'],
                    section=annotation['section'],
                    provider=annotation['provider'],
                )

                for tag in annotation['tags']:
                    print('>> {}: {}'.format(tag['name'], tag['uri']))

                    Tag.objects.get_or_create(
                        annotation=annotation_obj,
                        name=tag['name'],
                        uri=tag['uri'],
                    )

                print("")
