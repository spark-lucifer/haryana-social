from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Post(models.Model):
    body = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='dislikes', blank=True)
# Create your models here.
class Comment(models.Model):
    comment = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='comment_dislikes', blank=True)
class UserProfile(models.Model):
    user = models.OneToOneField(User,primary_key=True,verbose_name='user',related_name='profile', on_delete=models.CASCADE)
    name = models.CharField(max_length=100,blank=True,null=True)
    bio = models.TextField(max_length=500,blank=True,null=True)
    birth_date = models.DateField(null=True,blank=True)
    location = models.CharField(max_length=100,blank=True,null=True)
    profile_pic = models.ImageField(upload_to='uploads/profile_pictures',default='uploads/profile_pictures/default.jpg', blank=True)

class Game(models.Model):
   
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()

@receiver(post_save, sender=User)
def create_profile(sender,instance,created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender,instance,**kwargs):
    instance.profile.save()