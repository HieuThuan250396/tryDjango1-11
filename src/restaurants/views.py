from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from .models import RestaurantLocation
from django.db.models import Q
from .forms import RestaurantCreateForm, RestaurantLocationCreateForm
from .models import RestaurantLocation

# Create your views here.

@login_required(login_url="/login/")
def restaurant_createview(request):

    errors = None
    form = RestaurantLocationCreateForm(request.POST or None)
    if form.is_valid():
        if request.user.is_authenticated():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            return HttpResponseRedirect("/restaurants/")
        else:
            return HttpResponseRedirect("/login")
    if form.errors:
        errors = form.errors

    template_name = "restaurants/form.html"
    context = {"form": form, "errors": errors}
    return render(request, template_name, context)


class RestaurantListView(ListView):

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        if slug:
            queryset = RestaurantLocation.objects.all().filter(
                Q(category__iexact=slug) | Q(category__icontains=slug)
            )
        else:
            queryset = RestaurantLocation.objects.all()
        return queryset


class RestaurantDetailView(DetailView):
    queryset = RestaurantLocation.objects.all()


class RestaurantCreateView(LoginRequiredMixin, CreateView):
    form_class = RestaurantLocationCreateForm
    template_name = 'form.html'
    login_url = "/login/"
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        # instance.save()
        return super(RestaurantCreateView, self).form_valid(form)

    
    def get_context_data(self, *args, **kwargs):
        context = super(RestaurantCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Add Restaurant'
        return context
    