from django.db import models
from accounts.models import User


class Benefactor(models.Model):
    EXPERIENCE_CHOICES = (
        (0, "Beginner"),
        (1, "Intermediate"),
        (2, "Expert"),
    )

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experience = models.SmallIntegerField(choices=EXPERIENCE_CHOICES, default=0)
    free_time_per_week = models.PositiveSmallIntegerField(default=0)


class Charity(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    reg_number = models.CharField(max_length=10)


class TaskManager(models.Manager):
    '''In this function, return all tasks given to the desired user as charity in queryset format.
    For example, if the desired user was not a charity, obviously none of the tasks were given as charity and
     your function should return the value of nothing in the form of a queryset.'''

    def related_tasks_to_charity(self, user):
        return Task.objects.filter(charity=user.charity)

    '''In this function, return all the Tasks given to the target user as a benefactor in queryset format.
        For example, if the intended user was not a benefactor, then none of the tasks were given to him as
         a benefactor, and your function should return none in the form of a queryset.'''

    def related_tasks_to_benefactor(self, user):
        return Task.objects.filter(assigned_benefactor=user.benefactor)

    '''In this function, return all the Tasks that the intended user has access to in a queryset format.
        A user has access to Tasks that have been given to the intended user as a benefactor or given to the intended  
        user as charity or their status is Pending.
        The task of this function is to return all these tasks as a queryset.'''

    def all_related_tasks_to_user(self, user):
        return Task.objects.filter(assigned_benefactor=user.benefactor) | Task.objects.filter(
            charity=user.charity) | Task.objects.filter(state='P')


class Task(models.Model):
    STATE_CHOICES = (
        ('A', 'Assigned'),
        ('P', 'Pending'),
        ('W', 'waiting'),
        ('D', 'Done'),
    )

    id = models.AutoField(primary_key=True)
    assigned_benefactor = models.ForeignKey(Benefactor, on_delete=models.SET_NULL, null=True)
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE)
    age_limit_from = models.IntegerField(null=True, blank=True)
    age_limit_to = models.IntegerField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    gender_limit = models.CharField(max_length=1, null=True, blank=True)
    state = models.CharField(max_length=1, choices=STATE_CHOICES, default='P')
    title = models.CharField(max_length=60)

    objects = TaskManager()

