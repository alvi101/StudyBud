from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    participants = models.ManyToManyField(
        User, related_name="participants", blank=True)
    name = models.CharField(max_length=200)  # max len reqired for charfield()
    # this field in db can be blank, can be blank when submitting form
    description = models.TextField(null=True, blank=True)
    # participants =
    # take timestamp of current time
    updated = models.DateTimeField(auto_now=True)
    # auto now vs auto now add - add now is done only once when intialized
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ["-updated", "-created"]


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    # take timestamp of current time
    updated = models.DateTimeField(auto_now=True)
    # auto now vs auto now add - add now is done only once when intialized
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        print(self.body)
        return self.body[0:50]
