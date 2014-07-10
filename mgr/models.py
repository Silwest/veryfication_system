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

    def __unicode__(self):
        return '%s - %s ' % (self.field_of_study.name, self.name)


class Answer(models.Model):
    value = models.CharField(max_length=200, blank=False, null=False, default='Put your answer here!')
    correct = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s - %s ' % (self.id, self.value)


class Question(models.Model):
    question_number = models.IntegerField(default=0, blank=False, null=False)
    field_of_question = models.ForeignKey(FieldOfQuestion)
    value = models.CharField(max_length=400, blank=False, null=False, default='Put you question here!')
    image = models.ImageField(upload_to='attachments', blank=True, null=True)
    answer_1 = models.ForeignKey(Answer, related_name='answer_1', blank=True, null=True)
    answer_2 = models.ForeignKey(Answer, related_name='answer_2', blank=True, null=True)
    answer_3 = models.ForeignKey(Answer, related_name='answer_3', blank=True, null=True)
    answer_4 = models.ForeignKey(Answer, related_name='answer_4', blank=True, null=True)
    approved_by_admin = models.BooleanField(default=False, blank=True)

    def __unicode__(self):
        return '%s - %s ' % (self.field_of_question, self.value)