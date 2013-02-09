
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User



    
class Post(models.Model):
    
    def __unicode__(self):
        return self.owner.username
    
    post_category = (
        (u'music', u'Music'),
        (u'sports', u'Sports'),
        (u'education', u'Education'),
        (u'np', u'News & Politics'),
        (u'comedy', u'Comedy'),
        (u'technology', u'Technology'),
        (u'gaming', u'Gaming'),
        (u'fashion', u'Fashion'),
        (u'travel', u'Travel'),
    )
    
    date_time = models.DateTimeField(default=datetime.now())
    owner = models.ForeignKey(User)
    rating = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=10, choices=post_category)
    like = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=1024)
    
class Image_Post(Post):
    img = models.ImageField(upload_to='imgs', blank=False)
    
class URL_Post(Post):
    url = models.URLField(blank=False)
    
class Comment(models.Model):
    
    def __unicode__(self):
        return self.owner.username
    
    date_time = models.DateTimeField(default=datetime.now())
    owner = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    flag = models.PositiveIntegerField(default=0)
    description = models.CharField(unique=True, max_length=1024)














    
