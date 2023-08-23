from django.contrib import admin
from auctions.models import *

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    pass

class BidsAdmin(admin.ModelAdmin):
    pass

class CommentsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Comments, CommentsAdmin)
admin.site.register(Bids, BidsAdmin)
admin.site.register(Listings, ListingAdmin)