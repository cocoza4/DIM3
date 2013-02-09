
from cocoandco.models import Comment, Post, Image_Post, URL_Post
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
        return self.owner
    
    list_display= ('owner', 'category', 'like')
    list_filter = ['category', 'date_time', 'rating']
    search_fields = ['owner']
    date_hierarchy = "date_time"
    
class Image_PostAdmin(PostAdmin):
    pass

class URL_PostAdmin(PostAdmin):
    pass

admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Image_Post, Image_PostAdmin)
admin.site.register(URL_Post, URL_PostAdmin)


