from django.shortcuts import render
from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = 'index.html'

class SintomasView(TemplateView):
    template_name = 'sintomas.html'

class RecomendacoesView(TemplateView):
    template_name = 'recomendacoes.html'

class GraficosView(TemplateView):
    pass

class MitosView(TemplateView):
    template_name = 'mitos.html'

class FaqView(TemplateView):
    template_name = 'faq.html'