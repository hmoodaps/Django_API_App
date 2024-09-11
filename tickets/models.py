from django.conf import Settings, settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=50)
    hall = models.CharField(max_length=2)
    date = models.DateField()
    movie_time = models.TimeField()
    available_sets = models.IntegerField()
    all_sets = models.IntegerField()
    objects = models.Manager()



class Guest(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    set_num = models.IntegerField()
    objects = models.Manager()




class Reservation(models.Model):
    movie = models.ForeignKey(Movie, related_name='rez',on_delete=models.CASCADE)
    guest =  models.ForeignKey(Guest,  related_name='rez', on_delete=models.CASCADE)
    objects = models.Manager()


@receiver(post_save , sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

