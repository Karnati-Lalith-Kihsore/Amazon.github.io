from django.contrib import admin

# Register your models here.
from .models import User, Listing, Cart, Buy, User_details

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Cart)
admin.site.register(Buy)
admin.site.register(User_details)