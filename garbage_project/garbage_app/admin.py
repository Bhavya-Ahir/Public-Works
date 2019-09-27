from django.contrib import admin
from .models import Post,Vote,Garbage_User,Vote_table
# Register your models here.
admin.site.register(Post)
admin.site.register(Vote)
admin.site.register(Garbage_User)
admin.site.register(Vote_table)
