#from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
import uuid
import shortuuid

class Todo(models.Model):
   title = models.CharField(max_length=100)
   description = models.TextField()
   completed = models.BooleanField(default=False)

   def _str_(self):
     return self.title



class Event_Users(models.Model):
  user_id = models.AutoField(primary_key=True,editable=False)
  # models.Autofield(primary_key=True, editable=False, max_length=10)
  user_fname = models.CharField(max_length=30,null=True)
  user_lname = models.CharField(max_length=30,null=True)
  username = models.CharField(max_length=30,null=True)
  is_event_host = models.BooleanField(default=False)
  is_event_performer = models.BooleanField(default=False)
  is_event_guest = models.BooleanField(default=False)
  objects=models.Manager()

  def _str_(self):
    return self.Username


class Event_Socials(models.Model):
  social_id = models.AutoField(primary_key=True, editable=False)
  user_id = models.ForeignKey(Event_Users, on_delete=models.CASCADE,null=True)
  twitter = models.CharField(max_length=30,null=True)
  instagram = models.CharField(max_length=30,null=True)
  snapchat = models.CharField(max_length=30,null=True)
  Facebook = models.CharField(max_length=30,null=True)
  email = models.CharField(max_length=30,null=True)
  phone = models.CharField(max_length=10, null=True)
  user_bio = models.TextField(max_length=255,null=True)
  objects=models.Manager()


class Event(models.Model):
  event_id = models.AutoField(primary_key=True, editable=False)
  def short_unique():
    u = uuid.uuid4()
    s = shortuuid.encode(u)
    return s[:7]
  event_code = models.UUIDField(default = uuid.uuid4,
         editable = False)
  event_code_short = models.CharField(max_length=10, default=short_unique)
  event_name = models.CharField(max_length=55,null=True)
  event_location = models.CharField(max_length=30,null=True)
  event_org = models.CharField(max_length=30,null=True)
  host = models.ForeignKey(Event_Users, on_delete=models.CASCADE)
  event_social = models.ForeignKey(Event_Socials, on_delete=models.CASCADE,null=True)
  event_start_date = models.DateTimeField()
  event_end_date = models.DateTimeField()
  event_image = models.ImageField()
  about_event = models.TextField(max_length=500,null=True)
  objects=models.Manager()

class Event_Host(models.Model):
  host = models.ForeignKey(Event_Users, on_delete=models.CASCADE,null=True, editable=False)
  social = models.ForeignKey(Event_Socials, on_delete=models.CASCADE,null=True)
  event = models.ForeignKey(Event, on_delete=models.CASCADE,null=True)
  auth_user = models.CharField(max_length=50,null=True)
  objects=models.Manager()

  def _str_(self):
    return self.Username
 

class Event_Attendee(models.Model):
  event_id = models.ForeignKey(Event, on_delete=models.CASCADE,max_length=12, editable=False)
  user_id = models.ForeignKey(Event_Users, on_delete=models.CASCADE, max_length=12)
