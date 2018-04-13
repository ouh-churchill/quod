from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView

from .models import NewSession
from .models import NewVariable
from .models import NewCategory
from .models import NewSection
from .forms import SaveSession


def index(request):
    return HttpResponse("Hello, world. You're at the research variables index.")


class ViewAll(TemplateView):
    template_name = 'research_variables/view_all.html'

    def get_context_data(self, **kwargs):
        context = super(ViewAll, self).get_context_data(**kwargs)
        context['category'] = NewCategory.objects.all()  # .get() to do specific query
        context['section'] = NewSection.objects.all()
        context['session'] = NewSession.objects.all()
        context['variable'] = NewVariable.objects.all()
        context['form'] = SaveSession(self.request.POST or None)
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if context["form"].is_valid():
            print('Data collected')
        return super(TemplateView, self).render_to_response(context)

# Form creation ModelForm needs to be created do ensure collection of the data
# Formating data tables need to be created and conditional formating needs to be tested


class ViewAllPublic(TemplateView):
    template_name = 'research_variables/view_all_public.html'

    def get_context_data(self, **kwargs):
        context = super(ViewAllPublic, self).get_context_data(**kwargs)
        context['category'] = NewCategory.objects.all()  # .get() to do specific query
        context['section'] = NewSection.objects.all()
        context['session'] = NewSession.objects.all()
        context['variable'] = NewVariable.objects.all()
        return context


class ViewAllForm(ListView):
    model = NewSession
