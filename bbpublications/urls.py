"""bbpublications URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from europepmc.views import BiobankList, PublicationList
from europepmc.views import get_recommentation

urlpatterns = [
    path('admin/', admin.site.urls),
    path('biobanks/', BiobankList.as_view(), name='biobanks-list'),
    path('biobanks/<int:pk>/publications/', PublicationList.as_view(), name='publications-list'),
    path('biobanks/<int:pk>/publications/', PublicationList.as_view(), name='publications-list'),
    path('recommendation/<str:article_id>/', get_recommentation, name='recommendation-list'),
]
