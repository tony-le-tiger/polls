import datetime

from django.db import models
from django.utils import timezone

import validators

# You can find an example class diagram for the Model at
# http://yuml.me/edit/53759046
# You'll notice that the Model class provided by Django is 
# elided (it doesn't have the attributes or methods listed.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published',validators=[validators.not_future])
    def __unicode__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200,validators=[validators.not_unauthorized_word])
    votes = models.IntegerField(default=0)
    def __unicode__(self):
        return self.choice_text
