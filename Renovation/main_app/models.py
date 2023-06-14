from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=256, null=True)
    size = models.FloatField()

    def __str__(self):
        return self.name


class Purchase(models.Model):
    item = models.CharField(max_length=256)
    producer = models.CharField(max_length=256, null=True)
    price = models.FloatField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
