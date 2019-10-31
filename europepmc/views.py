from django.views.generic import ListView
from europepmc.models import Biobank, Publication
from .utils import calculate_recomendation
from django.shortcuts import render


class BiobankList(ListView):
    model = Biobank

    def get_queryset(self):
        queryset = Biobank.objects.with_publication()
        return queryset

class PublicationList(ListView):
    model = Publication

    def get_queryset(self):
        queryset = Publication.objects.filter(biobank__id=self.kwargs.get('pk'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        biobank = Biobank.objects.get(pk=self.kwargs.get('pk')) # the self.kwargs is different from **kwargs, and gives access to the named url parameters
        context['biobank'] = biobank
        return context

def get_recommentation(request, article_id):

    recommendation_list = calculate_recomendation(article_id)

    context = {
        'recommendation_list': recommendation_list[:5],
    }

    return render(request, 'europepmc/recommendation.html', context)
