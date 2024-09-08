from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=50)
    hall = models.CharField(max_length=2)
    date = models.DateField()
    movie_time = models.TimeField()
    available_sets = models.IntegerField()
    all_sets = models.IntegerField()


class Guest(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    set_num = models.IntegerField()



class Reservation(models.Model):
    movie = models.ForeignKey(Movie, related_name='rez',on_delete=models.CASCADE)
    guest =  models.ForeignKey(Guest,  related_name='rez', on_delete=models.CASCADE)

