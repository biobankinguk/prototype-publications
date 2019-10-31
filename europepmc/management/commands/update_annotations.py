from django.core.management.base import BaseCommand, CommandError

from europepmc.models import Biobank, Publication, Annotation, Tag

import pyodbc
import requests


class Command(BaseCommand):

    help = 'Import publications from EBI endpoint'

    def handle(self, *args, **options):

        articles_endpoint = 'https://www.ebi.ac.uk/europepmc/annotations_api/annotationsByArticleIds?articleIds={}:{}&format=JSON'

        biobanks = {}
        publications = {}

        for publication in Publication.objects.all():
        # for publication in Publication.objects.all()[:5]:

            r_articles = requests.get(articles_endpoint.format(publication.source, publication.pid))

            for annotation in r_articles.json()[0]['annotations']:

                try:
                    prefix=annotation['prefix']
                except KeyError:
                    prefix=''

                try:
                    exact=annotation['exact']
                except KeyError:
                    exact=''

                try:
                    aid=annotation['id']
                except KeyError:
                    aid=''

                try:
                    atype=annotation['type']
                except KeyError:
                    atype=''

                try:
                    section=annotation['section']
                except KeyError:
                    section=''

                try:
                    provider=annotation['provider']
                except KeyError:
                    provider=''

                print(publication.title)
                print(exact)
                print(aid)
                print(atype)
                print(section)
                print(provider)

                annotation_obj, created = Annotation.objects.get_or_create(
                    publication=publication,
                    exact=exact,
                    aid=aid,
                    atype=atype,
                    section=section,
                    provider=provider,
                )

                for tag in annotation['tags']:
                    print('>> {}: {}'.format(tag['name'], tag['uri']))

                    Tag.objects.get_or_create(
                        annotation=annotation_obj,
                        name=tag['name'],
                        uri=tag['uri'],
                    )

                print("")
