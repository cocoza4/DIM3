
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django import forms

post_category = (
        (u'music', u'Music'),
        (u'sport', u'Sport'),
        (u'education', u'Education'),
        (u'history', u'History'),
        (u'science', u'Science'),
        (u'politics', u'Politics'),
        (u'technology', u'Technology'),
        (u'economy', u'Economy'),
        (u'society', u'Society'),
        (u'world', u'World'),
    )    



class Post(models.Model):
    
    def __unicode__(self):
        return self.owner.username
    
    date_time = models.DateTimeField(default=datetime.now())
    owner = models.ForeignKey(User)
    rating = models.PositiveIntegerField(default=0)
    img = models.ImageField(upload_to='imgs', blank=True)
    like = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=1024)
    
class Choice(models.Model):
    
    def __unicode__(self):
        return self.post.title
    
    post = models.ForeignKey(Post)
    category = models.CharField(max_length=10, choices=post_category)

    
class Comment(models.Model):
    
    def __unicode__(self):
        return self.owner.username
    
    date_time = models.DateTimeField(default=datetime.now())
    owner = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    flag = models.PositiveIntegerField(default=0)
    description = models.CharField(max_length=1024)


# Model Forms
class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=256, help_text='Question')
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), help_text='Add a description', max_length=1024)
    categories = forms.MultipleChoiceField(widget = forms.SelectMultiple, 
                 choices = post_category, required = True, help_text='Choose categories')
    img = forms.ImageField(help_text='Upload a picture', required=False)
    
    
    class Meta:
        model = Post
        fields = ('categories', 'title','description', 'img', )
        
class CommentForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':3, 'id': 'text'}), help_text='Your comment', 
                                  required=True, max_length=1024)
    
    class Meta:
        model = Comment
        fields = ('description', )









    
