import datetime
from django.db import models
from django.db.models import signals, F
from django.utils import timezone
from django.template.defaultfilters import slugify

class User(models.Model):
    username = models.CharField(max_length=40)
    first_name = models.CharField(max_length=40)
    second_name = models.CharField(max_length=40)
    motto = models.CharField(max_length=100)
    image = models.ImageField(default='')
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unspecified')
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return self.username


class Hashtag(models.Model):
    name = models.CharField(max_length=30)
    occurences = models.IntegerField(default=0)

    def __str__(self):
        return self.name + ' (' + str(self.occurences) + ')'


class Tweet(models.Model):
    user = models.ForeignKey(User)
    text = models.CharField(max_length=160)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    def was_published_recently(self):
        return self.date_added >= timezone.now() - datetime.timedelta(days=1)

    def parse_hashtags(self):
        return [slugify(i) for i in self.text.split() if i.startswith("#")]

    def create_hashtags(self):
        hashtag_set = set(self.parse_hashtags())
        for hashtag in hashtag_set:
            h, created = Hashtag.objects.get_or_create(name=hashtag)
            h.save()
        Hashtag.objects.filter(name__in=hashtag_set).update(occurences=F('occurences')+1)

    def save(self):
        self.create_hashtags()
        super(Tweet, self).save()

# #SIGNALS
# def parse_hashtags(**kwargs):
#     instance = kwargs.get('instance')
#     set_of_hashtags = set(part[1:] for part in instance.text.split() if part.startswith('#'))
#     print(set_of_hashtags)
#     for hashtag in set_of_hashtags:
#         h, created = Hashtag.objects.get_or_create(name=hashtag)
#         h.save()
#     Hashtag.objects.filter(name__in=set_of_hashtags).update(occurences=F('occurences')+1)
#
#
# signals.post_init.connect(parse_hashtags, Tweet)


class Comment(models.Model):
    tweet = models.ForeignKey(Tweet)
    text = models.CharField(max_length=160)
    author = models.CharField(max_length=40)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author + ' added comment to tweet no. ' + self.tweet.text
