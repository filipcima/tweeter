from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
# Create your views here.


def index(request):
    addtweetform = AddTweet()
    context = {
        'tweets': Tweet.objects.order_by('-date_added')[:10],
        'add_tweet_form': addtweetform,
    }
    return render(request, 'feed.html', context)


def user(request, user_name):
    user = get_object_or_404(User, username=user_name)
    tweets = Tweet.objects.filter(user=user)

    context = {
        'user': user,
        'tweets': tweets
    }

    return render(request, 'user.html', context)


def tweet(request, id):
    tweet = get_object_or_404(Tweet, pk=id)
    comment_form = CommentForm()
    comments = Comment.objects.filter(tweet=id)
    context = {
        'tweet': tweet,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'tweet.html', context)


def discover(request):
    tweets = Tweet.objects.all()
    users = User.objects.all()
    context = {
        'users': users,
        'tweets': tweets,
    }
    return render(request, 'discover.html', context)


def popular(request):
    context = {
        'hashtags': Hashtag.objects.order_by('-occurences')[:5]
    }
    return render(request, 'popular.html', context)

def addcomment(request, id):
    tweet = get_object_or_404(Tweet, pk=id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            text = comment_form.cleaned_data['text']
            author = comment_form.cleaned_data['author']
            comment = Comment(text=text, author=author, tweet_id=id)
            comment.save()
    return redirect('tweet', id=tweet.pk)


def addtweet(request):
    if request.method == 'POST':
        addtweet = AddTweet(request.POST)
        if addtweet.is_valid():
            user = addtweet.cleaned_data['user']
            text = addtweet.cleaned_data['text']
            tweet = Tweet(text=text, user=user)
            tweet.save()
    return redirect('/')

def register(request):
    register_form = RegisterForm()
    context = {
        'register_form': register_form
    }
    return render(request, 'register.html', context)


def registernewuser(request):
    print("regnewuser()")
    if request.method == 'POST':
        print("req.method==post")
        register_user_form = RegisterForm(request.POST, request.FILES)

        if register_user_form.is_valid():
            username = register_user_form.cleaned_data['username']
            first_name = register_user_form.cleaned_data['first_name']
            second_name = register_user_form.cleaned_data['second_name']
            image = register_user_form.request.FILES['image']
            motto = register_user_form.cleaned_data['motto']
            gender = register_user_form.cleaned_data['gender']
            user = User(username=username, first_name=first_name, second_name=second_name, image=image, motto=motto, gender=gender)
            user.save()
    return redirect('register')


def hashtag(request, hash_name):
    hash_tag = get_object_or_404(Hashtag, name=hash_name)
    tweets = Tweet.objects.filter(text__contains=hash_name)

    context = {
        'hash_tag': hash_tag,
        'tweets': tweets
    }

    return render(request, 'hashtag.html', context)
