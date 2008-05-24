
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Announcement(models.Model):

    title = models.CharField(max_length=50)
    content = models.TextField()
    creator = models.ForeignKey(User)
    creation_date = models.DateTimeField()
    members_only = models.BooleanField()

    def get_absolute_url(self):
        return ("announcement_detail", [str(self.pk)])
    get_absolute_url = models.permalink(get_absolute_url)
    
    def __unicode__(self):
        return self.title
    
    class Admin:
        list_display = ("title", "creator", "creation_date", "members_only")
        list_filter = ("members_only",)
