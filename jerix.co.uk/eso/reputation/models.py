from django.db import models

# Create your models here.
class UserReputation(models.Model):
    """(UserReputation description)"""

    current_reputation = models.IntegerField(default=0)

    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return u"UserReputation"

class EntityReputation(models.Model):
    """
    This represents that ammount of reputation a voteable object has gained.
    This model will track the current reputation level and its voted history.
    """

    up_votes = models.ManyToManyField(UserReputation)
    down_votes = models.ManyToManyField(UserReputation)

    def current_vote(self):
        """docstring for current_reputation"""
        return self.up_votes.count() - self.down_votes.count()

    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return u"VoteReputation"

class ReputationReward(models.Model):
    """Represents a quatity of reputation that is given as a reward"""

    title = models.CharField(max_length=100)
    description = models.TextField(default='', blank=True)

    reputation_amount = models.IntegerField(default=0)

    class Admin:
        list_display = ('',)
        search_fields = ('title',)

    def __unicode__(self):
        return u'%s - %d' % (self.title, self.reputation_amount)


class ReputationMixIn(models.Model):
    """(ReputationMixIn description)"""

    reputation =  models.OneToOneField(EntityReputation, related_name='entity')
    reputation_owner = models.ForeignKey(UserReputation,
                                        related_name='votebles')

    class ReputationMeta:
        """
        Store information required by the reputation system, noteably how much
        an up_vote is valued for the entity owner.
        """
        up_vote_value = 0
        down_vote_value = 0

    class Meta:
        abstract = True
