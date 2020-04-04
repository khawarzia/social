from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


urlpatterns = [
    url(r'^$',views.home, name = "home"),
    url(r'login/', views.login_user, name = 'login'),
    url(r'^logout/$', views.logout_user, name= "logout"),

    #----------------------------------------------------------------------------
    url(r'^profile/(?P<user_name>\w+)/$', views.profile_user, name= "profile"),
    #---------------------------------------------------------------------------
    url(r'^register/$', views.register_user, name= "register"),
    url(r'^edit_profile/$', views.edit_profile, name = "edit_profile"),
    url(r'^dashbaord/$', views.dashboard, name = "dashboard"),
    
    #Password Change URL............
    url(r'^change_password/$', views.change_password, name = "change_password"),

    #password Reset URLS...........
    path('password_reset/', PasswordResetView.as_view(), name='password_reset' ),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    #Email Confirm URLs.....
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),

    #Contact Us Page ...
    url(r'^contact/$', views.contact, name="contact"),
    url(r'^search/$', views.search, name="search"),
    # Post page
    url(r'^post/$', views.PostView, name="post"),
    url(r'^subscribe/$', views.SubscriberView, name="subscribe"),
    url(r'^detail/(?P<id>\d+)/$', views.PostDetail, name="detail"),
    url(r'^edit/(?P<id>\d+)/$', views.PostFormEditView, name="edit"),


    path('social-post',views.social_post,name='social-post'),
    path('facebook-login',views.facebook_login,name='facebook-login'),
    path('facebook-change',views.facebook_change,name='facebook-change'),
    path('twitter-login',views.twitter_login,name='twitter-login'),
    path('twitter-change',views.twitter_change,name='twitter-change'),
    path('insta-login',views.insta_login,name='insta-login'),
    path('insta-change',views.insta_change,name='insta-change'),
]