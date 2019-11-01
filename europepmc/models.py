from django.db import models


class BiobankManager(models.Manager):

    def with_publication(self):

        result = []

        for biobank in Biobank.objects.all():

            if biobank.total_publication() > 0:

                result.append(biobank.id)

        return Biobank.objects.filter(id__in=result)


class Biobank(models.Model):

    name = models.CharField(
        max_length=128
    )

    exact_annotations = models.TextField(
        null=True,
        blank=True,
    )

    objects = BiobankManager()

    class Meta:
        ordering = ['name']


    def __str__(self):
        return self.name

    def total_publication(self):
        return Publication.objects.filter(biobank=self).count()


class Publication(models.Model):

    year = models.IntegerField(

    )

    title = models.CharField(
        max_length=256
    )

    biobank = models.ForeignKey(
        Biobank,
        on_delete=models.CASCADE,
        related_name='publications',
    )

    pid = models.CharField(
        max_length=256
    )

    source = models.CharField(
        max_length=256
    )

    doi = models.CharField(
        max_length=64
    )

    class Meta:
        ordering = ['-year', 'title']

    def __str__(self):
        return self.title


class Annotation(models.Model):

    publication = models.ForeignKey(
        Publication,
        related_name='annotations',
        on_delete=models.CASCADE
    )

    exact = models.CharField(
        max_length=256,
    )

    aid = models.CharField(
        max_length=256,
    )

    atype = models.CharField(
        max_length=256,
    )

    section = models.CharField(
        max_length=256,
    )

    provider = models.CharField(
        max_length=256,
    )


class Tag(models.Model):

    annotation = models.ForeignKey(
        Annotation,
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=256,
    )

    uri = models.CharField(
        max_length=256,
    )

