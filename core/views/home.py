from django.shortcuts import render
from core.models import Module
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class ModuleListView(ListView):
    model = Module
    template_name = 'home/home.html'
    context_object_name = 'modules'
    ordering = ['order']

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(name__icontains=q)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Module List'
        return context
        


