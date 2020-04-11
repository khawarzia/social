from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.core.mail import EmailMessage
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password
import string
import random

class profileModel(models.Model):
    user            = models.ForeignKey(get_user_model(), on_delete= models.CASCADE)
    contactNumber   = models.IntegerField(blank = True, null=True, default=0)
    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)
    class Meta:
        verbose_name = 'Profile'

class Post(models.Model):
    author           = models.ForeignKey(get_user_model(), on_delete= models.CASCADE)
    title            = models.CharField(max_length=150)
    message          = models.TextField(max_length=150)
    emails          = models.IntegerField()
    delivery_date    = models.DateField()
    created_on       = models.DateTimeField(auto_now_add=True)
    updated          = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    class Meta:
        ordering=['-created_on']

class Subscriber(models.Model):
    Name            = models.CharField(max_length=150)
    Email           = models.EmailField(max_length=150)
    Date_Subscribed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Email

# @receiver(post_save,sender=profileModel)
# def send_user_data_when_created_by_admin(sender, instance, **kwargs):

#       first_name = instance.user.username
#       print('first name is',first_name)
#       password = 'test0123456'
#       print(make_password(password))
#       email = instance.user.email
#       url='http://127.0.0.1:8000/login'
#       html_content = "your user name:%s <br> Password:%s <br> Login Here :%s "
#       message=EmailMessage(subject='welcome',body=html_content %(first_name,password,url),to=[email])
#       message.content_subtype='html'
#       message.send()


class twitter_handle(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    username = models.CharField(max_length=100,blank=True)
    password = models.CharField(max_length=200,blank=True)

    def __str__(self):
        return self.user.username

    def givepass(self,a):
        b = ''
        for i in a:
            b = b + i
            b = b + random.choice(string.ascii_letters+string.digits)
            b = b + random.choice(string.ascii_letters+string.digits)
            b = b + random.choice(string.ascii_letters+string.digits)
            b = b + random.choice(string.ascii_letters+string.digits)
            b = b + random.choice(string.ascii_letters+string.digits)
        self.password = b
        self.save()
        return self

    def getpass(self):
        a = ''
        b = 5
        for i in range(len(self.password)):
            if b == 5:
                a = a + self.password[i]
                b = b - 1
            elif b == 0:
                b = 5
            else:
                b = b - 1
        return a

class facebook_handle(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    username = models.CharField(max_length=100,blank=True)
    password = models.CharField(max_length=200,blank=True)

    def __str__(self):
        return self.user.username

    def givepass(self,a):
        b = ''
        for i in a:
            b = b + i
            b = b + random.choice(string.ascii_letters+string.digits)
            b = b + random.choice(string.ascii_letters+string.digits)
            b = b + random.choice(string.ascii_letters+string.digits)
            b = b + random.choice(string.ascii_letters+string.digits)
            b = b + random.choice(string.ascii_letters+string.digits)
        self.password = b
        self.save()
        return self

    def getpass(self):
        a = ''
        b = 5
        for i in range(len(self.password)):
            if b == 5:
                a = a + self.password[i]
                b = b - 1
            elif b == 0:
                b = 5
            else:
                b = b - 1
        return a

class insta_handle(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    username = models.CharField(max_length=100,blank=True)
    password = models.CharField(max_length=200,blank=True)

    def __str__(self):
        return self.user.username

    def givepass(self,a):
        b = ''
        for i in a:
            b = b + i
            b = b + random.choice(string.ascii_letters+string.digits)
            b = b + random.choice(string.ascii_letters+string.digits)
            b = b + random.choice(string.ascii_letters+string.digits)
            b = b + random.choice(string.ascii_letters+string.digits)
            b = b + random.choice(string.ascii_letters+string.digits)
        self.password = b
        self.save()
        return self

    def getpass(self):
        a = ''
        b = 5
        for i in range(len(self.password)):
            if b == 5:
                a = a + self.password[i]
                b = b - 1
            elif b == 0:
                b = 5
            else:
                b = b - 1
        return a

class email_handle(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    username = models.CharField(max_length=100,blank=True)
    password = models.CharField(max_length=200,blank=True)

    def __str__(self):
        return self.user.username

    def givepass(self,a):
        b = ''
        for i in a:
            b = b + i
            b = b + random.choice(string.ascii_letters+string.digits)
            b = b + random.choice(string.ascii_letters+string.digits)
            b = b + random.choice(string.ascii_letters+string.digits)
            b = b + random.choice(string.ascii_letters+string.digits)
            b = b + random.choice(string.ascii_letters+string.digits)
        self.password = b
        self.save()
        return self

    def getpass(self):
        a = ''
        b = 5
        for i in range(len(self.password)):
            if b == 5:
                a = a + self.password[i]
                b = b - 1
            elif b == 0:
                b = 5
            else:
                b = b - 1
        return a

class instaimg(models.Model):
    img = models.ImageField(verbose_name='Image for Instagram',upload_to='temp',default=None)

    def __str__(self):
        return ''