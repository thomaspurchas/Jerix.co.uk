import datetime

from django.db import models
from django.db.models.signals import post_save, pre_save
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from taggit.managers import TaggableManager

from accounts.models import AuthoredObject
from reputation.models import ReputationMixIn, create_entity_reputation
from modules.models import Module

# Create your models here.
class Question(ReputationMixIn, AuthoredObject):
    """(Question description)"""

    title = models.CharField(max_length=300)
    detail = models.TextField()
    asked = models.DateTimeField(default=datetime.datetime.now)
    tags = TaggableManager()

    @property
    def slug(self):
        return slugify(self.title)

    @property
    def current_vote(self):
        """docstring for vote"""
        return self.reputation.current_vote()

    @property
    def total_answers(self):
        """docstring for answers"""
        return self.answers.count()

    def __unicode__(self):
        return unicode(self.title)

    def get_absolute_url(self):
        """docstring for get_absolute_url"""
        return reverse('question', kwargs={'question_id': self.pk,
                        'slug':slugify(self.title)})

        class Meta:
            ordering = ['asked']

class Answer(AuthoredObject, ReputationMixIn):
    """(Answer description)"""

    question = models.ForeignKey(Question, related_name='answers')
    detail = models.TextField()

    @property
    def current_vote(self):
        """docstring for vote"""
        return self.reputation.current_vote()

    @property
    def slug(self):
        return u'answer-%s' % self.id

    def __unicode__(self):
        return u"%s - %s..." % (self.question.title, self.detail[:50])

    def get_absolute_url(self):
        return self.question.get_absolute_url() + u'#%s' % self.slug

def set_rep_to_author(sender, instance, *args, **kwargs):
    """docstring for set_rep_to_author"""
    instance.reputation_owner = instance.author

pre_save.connect(set_rep_to_author, Question)
pre_save.connect(set_rep_to_author, Answer)

post_save.connect(create_entity_reputation, Question)
post_save.connect(create_entity_reputation, Answer)