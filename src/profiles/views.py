from django.shortcuts import render
from django.http import Http404
from django.views.generic import DetailView, View, CreateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from restaurants.models import RestaurantLocation
from menus.models import Item

from .models import Profile
from .forms import RegisterForm

# Create your views here.

User = get_user_model()

def activate_user_view(request, code=None, *args, **kwargs):
    if code:
        act_profile_qs = ActivationProfile.objects.filter(key=code)
        if act_profile_qs.exists() and act_profile_qs.count() == 1:
            act_obj = act_profile_qs.first()
            if not act_obj.expired:
                user_obj = act_obj.user
                user_obj.is_active = True
                user_obj.save()
                act_obj.expired = True
                act_obj.save()
                return HttpResponseRedirect("/login")
    # invalid code
    return HttpResponseRedirect("/login")


class RegisterView(CreateView):
    form_class=RegisterForm
    template_name='registration/register.html'
    success_url = '/'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect("/logout")
        return super(RegisterView, self).dispatch(*args, **kwargs)
    

class ProfileFollowToggle(LoginRequiredMixin, View):
    def post(self, request, *argss, **kwargs):
        # print(request.data)
        # print(request.POST)
        username_to_toggle = request.POST.get("username")
        # print(user_to_toggle)
        profile, is_following = Profile.objects.toggle_follow(request.user, username_to_toggle)
        # print(profile.user.username)
        # print(is_following)
        return redirect(f"/u/{profile.user.username}/")

class ProfileDetailView(DetailView):
    template_name = "profiles/user.html"

    def get_object(self):
        username = self.kwargs.get("username")
        if username is None:
            raise Http404
        return get_object_or_404(User, username__iexact = username, is_active=True)

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(*args, **kwargs)
        # print(context)
        # user = self.get_object()
        user = context['user']
        is_following = False
        if user.profile in self.request.user.is_following.all():
            is_following = True
        context['is_following'] = is_following
        query = self.request.GET.get('q')
        item_exists = Item.objects.filter(user = user).exists()
        qs = RestaurantLocation.objects.filter(owner = user).search(query) 
        if qs.exists() and item_exists :
            context['locations'] = qs
        return context  