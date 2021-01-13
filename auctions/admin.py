from django.contrib import admin
from .models import auction, category,  bid,  comment,  User, activelisting

# Register your models here.
admin.site.register(auction)
admin.site.register(category)
admin.site.register(bid)
admin.site.register(comment)
admin.site.register(User)
admin.site.register(activelisting)
