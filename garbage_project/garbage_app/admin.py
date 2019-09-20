from django.contrib import admin
from .models import Post,Vote,Garbage_User,checkpoint,driver_checkpoint,checkpoint_dustbin
# Register your models here.
admin.site.register(Post)
admin.site.register(Vote)
admin.site.register(Garbage_User)
admin.site.register(checkpoint)
admin.site.register(driver_checkpoint)
admin.site.register(checkpoint_dustbin)
