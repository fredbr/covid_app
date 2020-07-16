from django.urls import path
from django.views.generic.base import RedirectView

from . import views

# configuracao
urlpatterns = [
    path(r'', RedirectView.as_view(url='/sintomas/')),
    path(r'sintomas/', views.SintomasView.as_view(), name='sintomas'),
    path(r'recomendacoes/', views.RecomendacoesView.as_view(), name='recomendacoes'),
    path(r'graficos/', views.GraficosView.as_view(), name='graficos'),
    path(r'mitos/', views.MitosView.as_view(), name='mitos'),
    path(r'faq/', views.FaqView.as_view(), name='faq'),
]
