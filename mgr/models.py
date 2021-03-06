from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=40, blank=False, null=False, default='Wydzial Fizyki i Informatyki Stosowanej')
    shortcut = models.CharField(max_length=10, blank=False, null=False, default='WFIIS')
    home_page = models.URLField(blank=False, null=False, default='http://www.ftj.agh.edu.pl/')

    def __unicode__(self):
        return self.name


class FieldOfStudy(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False, default='Informatyka Stosowana')
    department = models.ForeignKey(Department, default=1)

    class Meta:
        verbose_name_plural = 'Field of studies'

    def __unicode__(self):
        return self.name


class FieldOfQuestion(models.Model):
    name = models.CharField(max_length=40, blank=False, null=False, default='Dziedzina pytania')
    field_of_study = models.ForeignKey(FieldOfStudy)
    number_of_questions = models.IntegerField(default=0, blank=False, null=True)
    shortcut = models.CharField(max_length=5, blank=False, null=False, default='')

    def __unicode__(self):
        return '%s - %s ' % (self.field_of_study.name, self.name)


class Answer(models.Model):
    value = models.CharField(max_length=200, blank=False, null=False, default='Put your answer here!')
    correct = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s' % self.value


class Question(models.Model):
    question_number = models.IntegerField(default=0, blank=False, null=False)
    field_of_question = models.ForeignKey(FieldOfQuestion, related_name="fieldofquestion")
    value = models.CharField(max_length=255, unique=True, blank=False, null=False, default='Put you question here!')
    # image = models.ImageField(upload_to='attachments', blank=True, null=True)
    answer_1 = models.ForeignKey(Answer, related_name='A', blank=True, null=True)
    answer_2 = models.ForeignKey(Answer, related_name='B', blank=True, null=True)
    answer_3 = models.ForeignKey(Answer, related_name='C', blank=True, null=True)
    answer_4 = models.ForeignKey(Answer, related_name='D', blank=True, null=True)
    approved_by_admin = models.BooleanField(default=False, blank=True)
    is_prepared = models.BooleanField(default=False, blank=True)

    def __unicode__(self):
        return '%s - %s ' % (self.field_of_question, self.value)


class UserProfile(AbstractUser):
    question_prepared = models.ManyToManyField(Question, blank=True, related_name="prepared_by")


class CustomTest(models.Model):
    name = models.CharField(max_length=40, blank=False, null=False, unique=True, default='Przykladowy test')
    questions = models.ManyToManyField(Question, related_name="Pytania", verbose_name="questions")
    approved_by_admin = models.BooleanField(default=False, blank=True)


class Statistic(models.Model):
    correct_answers = models.IntegerField(default=0, blank=False, null=False)
    all_answers = models.IntegerField(default=0, blank=False, null=False)
    user = models.ForeignKey(UserProfile, related_name="user_stats")
    field_of_question = models.ForeignKey(FieldOfQuestion, blank=True, null=True, related_name="field_stats")
    date = models.DateTimeField(default=datetime.now, blank=True)

    def __unicode__(self):
        return "%s - %s - %s" % (self.user, self.field_of_question, self.date)