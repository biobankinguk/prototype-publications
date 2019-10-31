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

        # tsql = "SELECT name FROM organisations WHERE name='Northern Ireland Biobank (NIB)'"
        tsql = "SELECT name FROM organisations"
        with cursor.execute(tsql):

            row = cursor.fetchone()

            while row:

                Biobank.objects.get_or_create(
                    name=row[0]
                )

                row = cursor.fetchone()
                