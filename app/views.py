from django.shortcuts import render, redirect
from app.forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from app.models import *
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request, 'index.html')

def UserRegisterView(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'signup.html', {'form':form})


def ChatPage(request):
    user = User.objects.all()
    return render(request, 'home.html', {'user':user})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form':form})

def chat_view(request, username):
    user = User.objects.all()
    user1 = User.objects.get(username = username)
    user2 = User.objects.get(id = request.user.id)
    direct_messages = DirectMessage.objects.filter(
    (Q(sender=user1) & Q(receiver=user2)) |
    (Q(sender=user2) & Q(receiver=user1))
).order_by('timestamp')
    

    
    # print(request.user, username, oneuser)
    # chat = Chat.objects.get(participants= )
    # sender_msg = Message.objects.filter(chat = oneuser.id, sender = request.user)
    # receiver_msg = Message.objects.filter(chat = )
    # print(msg)
    # for i in msg:
    #     print(i.content,i.chat, i.sender, i.content)
    return render(request, 'home.html', {'user2':user1, 'user':user,'msg':direct_messages})

