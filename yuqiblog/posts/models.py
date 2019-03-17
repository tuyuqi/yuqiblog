from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models
from django.utils import timezone

#settings.AUTH_USER_MODEL
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='User')
    title = models.CharField(max_length=200)
    body = models.TextField(default='')
    created_date = models.DateTimeField(default=timezone.now)
    pub_date = models.DateTimeField()

    def publish(self):
        self.pub_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title



class Comment(models.Model):
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField(default='')
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text


def approved_comments(self):
    return self.comments.filter(approved_comment=True)





# Alternatives:
# class Post(models.Model):
#     title = models.CharField(max_length=255)
#     pub_date = models.DateTimeField()
#     #image = models.ImageField(upload_to='media/')
#     body = models.TextField()
#     #author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
#
#
#     def __str__(self):
#         return self.title
#
#     def pub_date_pretty(self):
#         return self.pub_date.strftime('%b %e %Y')
#
#     def summary(self):
#         return self.body[:100]
