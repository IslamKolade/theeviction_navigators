from django.contrib import admin
from .models import The_Eviction_Navigators, Contact_Form_Submission
# Register your models here.
class Contact_Filter(admin.ModelAdmin): 
    search_fields = ('name',)


admin.site.register(The_Eviction_Navigators)
admin.site.register(Contact_Form_Submission, Contact_Filter)

admin.site.site_header = 'The Eviction Navigators Admin'
admin.site.site_title = 'The Eviction Navigators Admin Panel'
admin.site.index_title = 'Welcome to The Eviction Navigators Admin'