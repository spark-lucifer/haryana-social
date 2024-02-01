from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class LinkPost(models.Model):
    title = models.CharField(max_length=100)
    link = models.URLField(blank=True)
    link1 = models.URLField(blank=True)
    link2 = models.URLField(blank=True)
    body = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_linkposts')