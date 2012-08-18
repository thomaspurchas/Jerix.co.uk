from django.db import models
from django.contrib.auth.models import User
from accounts.models import UserProfile

# Create your models here.
class EntityReputation(models.Model):
    """
    This represents that ammount of reputation a voteable object has gained.
    This model will track the current reputation level and its voted history.
    """

    up_votes = models.ManyToManyField(UserProfile, related_name='votes_up')
    down_votes = models.ManyToManyField(UserProfile, related_name='votes_down')

    def current_vote(self):
        """docstring for current_reputation"""
        return self.up_votes.count() - self.down_votes.count()

    def vote_up(self, UserProfile):
        self.down_votes.remove(UserProfile)
        self.up_votes.add(UserProfile)

    def vote_down(self, UserProfile):
        self.up_votes.remove(UserProfile)
        self.vote_down.add(UserProfile)

    def __unicode__(self):
        return u"VoteReputation"

class ReputationReward(models.Model):
    """Represents a quatity of reputation that is given as a reward"""

    title = models.CharField(max_length=100)
    description = models.TextField(default='', blank=True)

    reputation_amount = models.IntegerField(default=0)

    def __unicode__(self):
        return u'%s - %d' % (self.title, self.reputation_amount)


class ReputationMixIn(models.Model):
    """(ReputationMixIn description)"""

    reputation = models.OneToOneField(EntityReputation, related_name='+', null=True)
    reputation_owner = models.ForeignKey(User, related_name='+')

    def vote_up(self, User):
        self.reputation.vote_up(User.get_profile())

    def vote_down(self, User):
        self.reputation.vote_down(User.get_profile())

    def set_reputation_owner(self, user):
        """Set the reputation owner based on a user object"""
        profile = user.get_profile()
        self.reputation_owner = profile

    class ReputationMeta:
        """
        Store information required by the reputation system, noteably how much
        an up_vote is valued for the entity owner.
        """
        up_vote_value = 5
        down_vote_value = 5

    class Meta:
        abstract = True

def create_entity_reputation(sender, instance, created, **kwargs):
    if created:
        rep = EntityReputation.objects.create()
        instance.reputation = rep
        instance.save()