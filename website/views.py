from django.shortcuts import render
from django.views.generic import TemplateView
from .plots.plot import plots_list

class IndexView(TemplateView):
    template_name = 'index.html'

class SintomasView(TemplateView):
    template_name = 'sintomas.html'

class RecomendacoesView(TemplateView):
    template_name = 'recomendacoes.html'

class GraficosView(TemplateView):
    template_name = 'graficos.html'

    def get_context_data(self, **kwargs):
        context = super(GraficosView, self).get_context_data(**kwargs)
        context['plots'] = plots_list()
        return context

class MitosView(TemplateView):
    template_name = 'mitos.html'

class FaqView(TemplateView):
    template_name = 'faq.html'