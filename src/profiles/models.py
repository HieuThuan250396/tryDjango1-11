from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from .utils import code_generator
from django.core.mail import send_mail

User = settings.AUTH_USER_MODEL

# Create your models here.

class ProfileManage(models.Manager):
    def toggle_follow(self, request_user, username_to_toggle):
        # print(user_to_toggle)
        profile = Profile.objects.get(user__username__iexact=username_to_toggle)
        user = request_user
        is_following = False
        # print("USER " + user.username)
        # print("PROFILE " + profile.user.username)
        if user in profile.followers.all():
            profile.followers.remove(user)
        else:
            profile.followers.add(user)
            is_following = True
        return profile, is_following


class Profile(models.Model):
    user            = models.OneToOneField(User)
    followers       = models.ManyToManyField(User, related_name='is_following', blank=True)
    # following     = models.ManyToManyField(User, related_name='user_following', blank=True)
    activation_key  = models.CharField(max_length=120, blank=True, null=True)
    activated       = models.BooleanField(default=False)
    timestamp       = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)

    objects = ProfileManage()

    def __str__(self):
        return self.user.username

    def send_activation_email(self):
        print("Activating")
        if self.activated :
            self.activation_key = code_generator()
            self.save()
            # path = 
            subject = 'Activate your account'
            from_email = settings.DEFAULT_FROM_EMAIL
            message = f'Activate your account here : {self.activation_key}'
            recipient_list = [self.user.email]
            html_message = f'<p>Activate your account here : {self.activation_key}<p>'
            sent_mail = send_mail(
                subject, message, 
                from_email, 
                recipient_list, 
                fail_silently=False, 
                html_message=html_message)
            return send_mail
        

def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        profile, is_created = Profile.objects.get_or_create(user=instance)
        default_user_profile = Profile.objects.get_or_create(user__id=1)[0]
        default_user_profile.followers.add(instance)


        profile.followers.add(2)

post_save.connect(post_save_user_receiver, sender=User)