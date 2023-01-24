from django.shortcuts import render, redirect
from .models import Manager

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import login

from django.urls import reverse_lazy

# Create your views here.

class login(LoginView):
	template_name = 'mainApp/login.html'
	fields= '__all__'
	redirect_authenticated_user = True

	def get_success_url(self):
		return reverse_lazy('appList')
        
class register(FormView):
    template_name = 'mainApp/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        return super( register, self ).form_valid( form )


class appList(LoginRequiredMixin, ListView):
    model = Manager
    context_object_name = 'manager'

    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        context ['manager'] = context ['manager'].filter( user = self.request.user )

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['manager'] = context['manager'].filter(
                title__startswith = search_input
            )

        context['search-input'] = search_input

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        for item in queryset:
            item.hidden_password = '*' * len(item.password)
            item.save()
        return queryset

class appDetail(LoginRequiredMixin, DetailView):
    model = Manager
    context_object_name = 'manager'

class appCreate(LoginRequiredMixin, CreateView):
    model = Manager
    fields = ['title', 'password']
    success_url = reverse_lazy('appList')

    def form_valid( self, form ):
        form.instance.user = self.request.user
        return super(appCreate, self).form_valid(form)

class appUpdate(LoginRequiredMixin, UpdateView):
    model = Manager
    fields = ['password']
    success_url = reverse_lazy('appList')

class appDelete(LoginRequiredMixin, DeleteView):
    model = Manager
    context_object_name = 'manager'
    success_url = reverse_lazy('appList')
