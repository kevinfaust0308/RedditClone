from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=200)
    url = models.TextField()
    pub_date = models.DateTimeField()
    author = models.ForeignKey(User)
    votes = models.IntegerField(default=1)

    def __str__(self):
        return 'Title: ' + self.title + ' Author: ' + self.author.username

    def get_username(self):
        return self.author.username

    def get_pretty_date(self):
        return self.pub_date.strftime('%b %d, %Y')

    def get_full_url(self):
        url = self.url
        prefix = 'http://'
        sprefix = 'https://'

        if not url.startswith(prefix) or not url.startswith(sprefix):
            url = prefix + url
        return url