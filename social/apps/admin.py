from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.admin import AdminSite

class MyAdminSite(AdminSite):
    site_header = 'Compaigns Admin'
    site_title  = 'Compaigns '
    index_title = 'Compaigns '
 
my_admin_site = MyAdminSite(name='Compaigns')

class profileAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'contactNumber']
    search_fields = ['id', 'user__username', 'user__first_name', 'user__last_name', ]

class PostAdmin(admin.ModelAdmin):
    list_display = ['title','message', 'created_on']

class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['Name','Email', 'Date_Subscribed']


my_admin_site.register(Group, GroupAdmin)
my_admin_site.register(User, UserAdmin)
my_admin_site.register(profileModel, profileAdmin)

my_admin_site.register(Post, PostAdmin)
my_admin_site.register(Subscriber, SubscriberAdmin)

my_admin_site.register(twitter_handle)
my_admin_site.register(facebook_handle)
my_admin_site.register(insta_handle)

my_admin_site.register(email_handle)

