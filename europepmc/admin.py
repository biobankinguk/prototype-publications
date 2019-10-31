from django.contrib import admin


from europepmc.models import Biobank, Publication, Annotation, Tag


class PublicationInline(admin.TabularInline):
    model = Publication


@admin.register(Biobank)
class BiobankAdmin(admin.ModelAdmin):
    inlines = [
        PublicationInline
    ]

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    pass

@admin.register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

