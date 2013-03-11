
from cocoandco.models import Comment, Post, Choice, Member
from django.contrib import admin

    
class CommentAdmin(admin.ModelAdmin):
    
    def __unicode__(self):
        return self.owner
    
    list_display= ('owner', 'description', 'flag')
    list_filter = ['date_time']
    search_fields = ['owner']
    date_hierarchy = "date_time"
    
class PostAdmin(admin.ModelAdmin):
    
    def __unicode__(self):
        return self.title
    
    list_display= ('owner', 'like')
    list_filter = ['date_time', 'rating']
    search_fields = ['owner']
    date_hierarchy = "date_time"

admin.site.register(Choice)
admin.site.register(Member)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)


