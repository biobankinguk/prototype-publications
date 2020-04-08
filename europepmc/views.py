from django.views.generic import ListView
from django.shortcuts import render
from europepmc.models import Biobank, Publication
from .utils import calculate_recomendation_by_publication
from .utils import search_publications


class BiobankList(ListView):
    """
    List all biobanks
    """
    model = Biobank

    def get_queryset(self):
        queryset = Biobank.objects.with_publication()
        return queryset


class PublicationList(ListView):
    """
    List publications of a biobank
    """
    model = Publication

    def get_queryset(self):
        queryset = Publication.objects.filter(biobank__id=self.kwargs.get('pk'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # the self.kwargs is different from **kwargs, and gives access to the named url parameters
        biobank = Biobank.objects.get(pk=self.kwargs.get('pk'))

        context['biobank'] = biobank
        return context


def get_publications(request, pk):
    """
    List publications of a biobank (duplicate?)
    """

    biobank = Biobank.objects.get(pk=pk)

    publication_list = Publication.objects.filter(biobank=biobank)

    result = []

    for p in publication_list:

        annotation_list = p.annotations.all()

        exact_set = set()

        for a in annotation_list:

            exact_set.add(a.exact.lower())

        obj = {
            'year': p.year,
            'title': p.title,
            'doi': p.doi,
            'annotations': ', '.join(sorted(exact_set))
        }

        result.append(obj)

    context = {
        'object_list': result,
        'biobank': biobank
    }

    return render(request, 'europepmc/publication_list.html', context)


def get_recommentation(request, article_id):
    """
    List recomendations given an article
    """

    recommendation_list = calculate_recomendation_by_publication(article_id)

    context = {
        'recommendation_list': recommendation_list[:5],
    }

    return render(request, 'europepmc/recommendation.html', context)


def search(request):
    """
    Search publications given a keyword
    """

    search_text = None
    result = None

    if request.method == 'POST':
        search_text = request.POST.get('search_text')
        result = search_publications(search_text)

    context = {
        'search_text': search_text,
        'result': result,
    }

    return render(request, 'europepmc/search.html', context)
