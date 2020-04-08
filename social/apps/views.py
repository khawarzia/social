from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import *
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage,get_connection
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import *
from django.urls import reverse
from django.db.models import Q
from mysite.settings import BASE_DIR
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import instabot
import os

def handler404(request):
    return render(request, '404.html', status=404)

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return render(request, 'music/home.html', )

@login_required()
def dashboard(request):
    posts=Post.objects.filter(author=request.user)
    context={
        'post':posts
    }
    return render(request, 'music/dashboard.html',context)

def social_post(request):
    template = 'social/new-post.html'
    context = {}
    form = imageform(request.POST or None,request.FILES or None)
    try:
        fbobj = facebook_handle.objects.get(user=request.user)
        context['fbobj'] = fbobj
        print(fbobj.getpass())
    except:
        fbobj = None
        context['fbobj'] = False
    try:
        twobj = twitter_handle.objects.get(user=request.user)
        context['twobj'] = twobj
        print(twobj.getpass())
    except:
        twobj = None
        context['twobj'] = False
    try:
        inobj = insta_handle.objects.get(user=request.user)
        context['inobj'] = inobj
        print(inobj.getpass())
    except:
        inobj = None
        context['inobj'] = False
    context['check321'] = fbobj or (twobj or inobj)
    if request.method == 'POST':
        a = request.POST['post-content']
        try:
            b = request.POST['facebook']
        except:
            b = 'off'
        try:
            c = request.POST['twitter']
        except:
            c = 'off'
        try:
            d = request.POST['instagram']
        except:
            d = 'off'
        if b == 'on' and fbobj != None:
            context['ret1'] = add_to_fb(fbobj.username,fbobj.getpass(),a)
            if request.POST['page_url'] and context['ret1'] == 'Post made successfully on facebook':
                post_to_fb_page(fbobj.username,fbobj.getpass(),a,request['page_url'])
        if c == 'on' and twobj != None:
            context['ret2'] = add_to_twitter(twobj.username,twobj.getpass(),a,request.POST['verify'])
            if context['ret2'] == 'Please enter the verification code send to you by twitter':
                context['verifycheck'] = True
            else:
                context['verifycheck'] = False
        if d == 'on' and inobj != None:
            if form.is_valid():
                form.save()
                obj = instaimg.objects.last()
                k = obj.img.name
                k = strip6(BASE_DIR) + '\\media\\temp\\'+ k.split('/')[1]
                context['ret3'] = add_to_insta(inobj.username,inobj.getpass(),a,k)
                obj.delete()
                try:
                    os.remove(k+'.REMOVE_ME')
                except:
                    pass
            else:
                context['ret3'] = 'Please select an image in order to post on Instagram'
    form = imageform()
    context['form'] = form
    return render(request,template,context)

def strip6(a):
    return a[0:len(a)-7]

def facebook_login(request):
    template = 'social/login.html'
    context = {}
    if request.method == 'POST':
        a = request.POST['username']
        b = request.POST['password']
        obj = facebook_handle()
        obj.user = request.user
        obj.username = a
        obj.save()
        obj.givepass(b)
        return redirect('/social-post')
    return render(request,template,context)

def twitter_login(request):
    template = 'social/login.html'
    context = {}
    if request.method == 'POST':
        a = request.POST['username']
        b = request.POST['password']
        obj = twitter_handle()
        obj.user = request.user
        obj.username = a
        obj.save()
        obj.givepass(b)
        return redirect('/social-post')
    return render(request,template,context)

def insta_login(request):
    template = 'social/login.html'
    context = {}
    if request.method == 'POST':
        a = request.POST['username']
        b = request.POST['password']
        obj = insta_handle()
        obj.user = request.user
        obj.username = a
        obj.save()
        obj.givepass(b)
        return redirect('/social-post')
    return render(request,template,context)

def facebook_change(request):
    template = 'social/login.html'
    context = {'name':facebook_handle.objects.get(user=request.user).username}
    if request.method == 'POST':
        a = request.POST['username']
        b = request.POST['password']
        obj = facebook_handle.objects.get(user=request.user)
        obj.username = a
        obj.save()
        obj.givepass(b)
        return redirect('/social-post')
    return render(request,template,context)

def twitter_change(request):
    template = 'social/login.html'
    context = {'name':twitter_handle.objects.get(user=request.user).username}
    if request.method == 'POST':
        a = request.POST['username']
        b = request.POST['password']
        obj = twitter_handle.objects.get(user=request.user)
        obj.username = a
        obj.save()
        obj.givepass(b)
        return redirect('/social-post')
    return render(request,template,context)

def insta_change(request):
    template = 'social/login.html'
    context = {'name':insta_handle.objects.get(user=request.user).username}
    if request.method == 'POST':
        a = request.POST['username']
        b = request.POST['password']
        obj = insta_handle.objects.get(user=request.user)
        obj.username = a
        obj.save()
        obj.givepass(b)
        return redirect('/social-post')
    return render(request,template,context)

def login_user(request):
    if request.method!= 'POST':
        form = loginForm()
    else:
        form = loginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username = form.cleaned_data['username'], password = form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.warning(request, 'Usename or password may have been entered incorrectly.')
                return redirect('login')
    return render(request, 'music/login.html', {'form' : form})

def logout_user(request):
    logout(request)
    return redirect('home')

@login_required()
def profile_user(request, user_name):
    message = ''
    try:
        user = User.objects.get(username = user_name)
        editProfile = False
        #print(request.user.username == user_name)
        if (request.user==user):
            if request.user.is_superuser:
                contactNumber = None
                editProfile = True
            else:
                contactNumber  = profileModel.objects.get(user = user).contactNumber
                editProfile = True
        else:
            if request.user.is_superuser:
                contactNumber  = profileModel.objects.get(user = user).contactNumber
                editProfile = False
            else:
                contactNumber = None
                editProfile = None
    except:
        user=request.user
        if request.user.is_superuser:
            contactNumber = None
            editProfile = True
            message = user_name + " Doest Not Exists "
        else:
            contactNumber  = profileModel.objects.get(user = User.objects.get(username = request.user.username)).contactNumber
            editProfile = True
            message = user_name
    return render(request, 'music/profile.html', {'contactNumber': contactNumber,'editProfile' :editProfile, 'user':user, 'message' : message})
    
def register_user(request):
    if request.method!='POST':
        form = registerForm()
        form_2 = profileInformForm()
    else:
        form = registerForm(request.POST)
        form_2 = profileInformForm(request.POST)
        if form.is_valid() & form_2.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.set_password(form.cleaned_data['password2'])
            user.email = form.cleaned_data['email'].lower()
            user.save()
            profile = profileModel.objects.create(user = user)
            profile.contactNumber = form_2.cleaned_data['contactNumber']
            profile.save()
            current_site = get_current_site(request)
            message = render_to_string('music/acc_active_email.html', {
                'user':user, 'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your account.'
            to_email = form.cleaned_data.get('email').lower()
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request, 'music/acc_active_email_confirm.html')
    return render(request, 'music/register.html', {'form' : form, 'form_2' : form_2})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')

@login_required()
def edit_profile(request):
    try:
        profile = profileModel.objects.get(user=request.user)
    except profileModel.DoesNotExist :
        profile = profileModel.objects.create(user=request.user)
        profile.save()
    if request.method!='POST':
        form = EditProfileForm(instance = request.user)
        form_2 = profileInformForm(instance=profile)
    else:
        # print(request.POST)
        form_2 = profileInformForm(request.POST,instance=profile)
        form = EditProfileForm(request.POST, instance = request.user)
        if form.is_valid() and form_2.is_valid():
            form.save()
            form_2.save()
            return HttpResponseRedirect(reverse('profile', args=[request.user.username]))
    return render(request, 'music/edit_profile.html',{'form' : form, 'profile':profile, 'form_2':form_2})

@login_required()
def change_password(request):
    if request.method!='POST':
        form = PasswordChangeForm(user = request.user)
    else:
        form = PasswordChangeForm(data = request.POST, user = request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(reverse('profile', args=[request.user.username]))
    return render(request, 'music/change_password.html' , {'form': form})

def contact(request):
    if request.method!='POST':
        form = contactForm()
    else:
        form = contactForm(request.POST)
        if form.is_valid():
            mail_subject = 'Contact -- By -- ' + form.cleaned_data.get('userName')
            to_email = settings.EMAIL_HOST_USER
            message = form.cleaned_data.get('body')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return redirect('home')
    
    context= {'form' : form}
    return render(request, 'music/contact.html', context)


def search(request):

    query = request.GET.get('query', None)
    search_user = Post.objects.all()
    if query is not None:
        search_user = search_user.filter(
            Q(author__username__icontains=query) |
            Q(title__icontains=query) |
            Q(message__icontains=query) 
    

        )
    print(query)
 
    context = {

        'search_user': search_user,
        'query':query
     
    }

    return render(request, 'music/search.html', context)


def PostView(request):
    form=PostForm()
    if request.method == 'POST':
        form=PostForm(request.POST,request.FILES)
        if form.is_valid(): 
            new = form.save(commit=False)
            new.author=request.user
          ########### Emails ####################
            current_site = get_current_site(request)
            message = render_to_string('music/compaign.html', {
                'title':request.POST['title'], 'domain':current_site.domain,
                'message': request.POST['message'],
            })
            mail_subject = request.POST['title']
            subs=Subscriber.objects.all()
            emails=[]
            for i in subs:
                emails.append(i.Email)
            if request.POST['user'] and request.POST['pass']:
                try:
                    obj = email_handle.objects.get(user=request.user)
                    obj.username = request.POST['user']
                    obj.save()
                    obj.givepass(request.POST['pass'])
                    obj.save()
                except:
                    obj = email_handle()
                    obj.user = request.user
                    obj.username = request.POST['user']
                    obj.save()
                    obj.givepass(request.POST['pass'])
                    obj.save()
            else:
                obj = email_handle.objects.get(user=request.user)
            con = get_connection(host='smtp.gmail.com',port=587,username=obj.username,password=obj.getpass(),use_tls=True)
            email = EmailMessage(mail_subject, message, to=[emails],from_email=obj.username, connection=con)
            email.send()
            con.close()
            ######################################
            new.emails = len(emails)
            new.save()
            form.save()
            return redirect('dashboard')
    context={
        'form':form
    }
    try:
        obj = email_handle.objects.get(user=request.user)
        context['emobj'] = obj
    except:
        context['emobj'] = False
    return render(request,'music/postview.html',context)



def PostFormEditView(request,id):
    obj= Post.objects.get(id=id)
    form= PostFormEdit(instance=obj)
    if request.method=='POST':
        form=PostFormEdit(request.POST , instance=obj )
        if form.is_valid():
            new = form.save(commit=False)
            new.author=request.user
            new.save()
            form.save()
            return redirect('dashboard')
    context={
        'form':form,  
        'object':obj 
    }
    return render(request,'music/postviewedit.html',context)

from .utils import *


def PostDetail(request,id):
    posts=Post.objects.get(id=id)
    api=get_api(request)
    print(api)
    # status = api.update_status(status='chachi') 
    context={
        'posts':posts
    }
    return render(request,'music/postdetail.html',context)


def SubscriberView(request):
    form=SubscriberForm()
    if request.method == 'POST':
        form=SubscriberForm(request.POST,request.FILES)
        if form.is_valid(): 
            new = form.save(commit=False)
            new.author=request.user
            new.save()
            form.save()
            return redirect('dashboard')
    context={
        'form':form
    }
    return render(request,'music/subscriberview.html',context)



def add_to_fb(name,passs,post_content):
    cd_url = '/usr/bin/chromedriver'
    opt = webdriver.ChromeOptions()
    opt.add_argument('--headless')
    opt.add_argument('--no-sandbox')
    opt.add_experimental_option('excludeSwitches',['enable-automation'])
    driver = webdriver.Chrome(executable_path=cd_url,options=opt)
    driver.get('https://web.facebook.com/')
    # start login
    while True:
        try:
            driver.find_element_by_xpath('//*[@id="email"]').send_keys(name)
            driver.find_element_by_xpath('//*[@id="pass"]').send_keys(passs)
            break
        except:
            time.sleep(1)
    driver.find_element_by_xpath('//*[@id="u_0_b"]').click()
    # end login
    start_time = time.time()
    # start post
    while True:
        try:
            elems = driver.find_elements_by_tag_name('textarea')
            elems[0].send_keys(post_content)
            break
        except:
            time.sleep(1)
            if (time.time() - start_time >= 25):
                return 'Facebook credentials are not correct!'
    while True:
        try:
            elems = driver.find_elements_by_tag_name('button')
            for i in elems:
                if i.text == 'Post':
                    i.click()
            break
        except:
            pass
    # end post
    time.sleep(5)
    driver.quit()
    return ('Post made successfully on facebook')

def add_to_twitter(name,passs,post_content,verify):
    cd_url = '/usr/bin/chromedriver'
    opt = webdriver.chrome.options.Options()
    opt.add_argument('--headless')
    opt.add_argument('--no-sandbox')
    opt.add_experimental_option('excludeSwitches',['enable-automation'])
    driver = webdriver.Chrome(executable_path=cd_url,options=opt)
    driver.get('https://twitter.com/login')
    # start login
    while True:
        try:
            driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/form/div/div[1]/label/div/div[2]/div/input').send_keys(name)
            driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/form/div/div[2]/label/div/div[2]/div/input').send_keys(passs)
            break
        except:
            time.sleep(1)
    driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/form/div/div[3]/div/div/span/span').click()
    # end login
    time.sleep(5)
    if verify:
        driver.find_element_by_id('challenge_response').send_keys(verify)
        driver.find_element_by_id('email_challenge_submit').click()
        time.sleep(5)
    if '/login/error' in driver.current_url:
        return 'Twitter credentials are not correct'
    if '/account/login_challenge' in driver.current_url:
        return 'Please enter the verification code send to you by twitter'
    # start tweet
    while True:
        try:
            driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div').send_keys(post_content)
            break
        except:
            time.sleep(1)
    driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div/div[2]/div[3]/div').click()
    # end tweet
    time.sleep(5)
    driver.quit()
    return ('Post made successfully on twitter')

def add_to_insta(name,passs,post_content,image_to_post):
    bot = instabot.Bot()
    try:
        bot.login(username=name,password=passs,proxy=None)
    except:
        return ('Instagram credentials are not correct!')
    bot.upload_photo(image_to_post,caption=post_content)
    return ('Post made successfully on Instagram')

def post_to_fb_page(name,passs,post_content,page_name):
    cd_url = '/usr/bin/chromedriver'
    opt = webdriver.ChromeOptions()
    opt.add_argument('--headless')
    opt.add_argument('--no-sandbox')
    opt.add_experimental_option('excludeSwitches',['enable-automation'])
    driver = webdriver.Chrome(executable_path=cd_url,options=opt)
    driver.get('https://mbasic.facebook.com/'+page_name+'/')
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="mobile_login_bar"]/div[2]/a[2]').click()
    while True:
        try:
            driver.find_element_by_xpath('//*[@id="m_login_email"]').send_keys(name)
            driver.find_element_by_xpath('//*[@id="login_form"]/ul/li[2]/div/input').send_keys(passs)
            break
        except:
            time.sleep(1)
    driver.find_element_by_xpath('//*[@id="login_form"]/ul/li[3]/input').click()
    while True:
        try:
            elems = driver.find_elements_by_tag_name('textarea')
            elems[0].send_keys(post_content)
            break
        except:
            time.sleep(1)
    while True:
        try:
            driver.find_element_by_xpath('//*[@id="mbasic-composer-form"]/table/tbody/tr/td[3]/div/input').click()
            break
        except:
            pass
    time.sleep(5)
    driver.quit()
    return
