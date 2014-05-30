from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=40, blank=False, null=False, default='Wydzial Fizyki i Informatyki Stosowanej')
    shortcut = models.CharField(max_length=10, blank=False, null=False, default='WFIIS')
    home_page = models.URLField(blank=False, null=False, default='http://www.ftj.agh.edu.pl/')

    def __unicode__(self):
        return self.name


class FieldOfStudy(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False, default='Informatyka Stosowana')

    class Meta:
        verbose_name_plural = 'Field of studies'

    def __unicode__(self):
        return self.name


class FieldOfQuestion(models.Model):
    name = models.CharField(max_length=40, blank=False, null=False, default='Dziedzina pytania')
    field_of_study = models.ForeignKey(FieldOfStudy)

    def __unicode__(self):
        return '{1} - {2}'.format(self.field_of_study, self.name)


class Answer(models.Model):
    value = models.CharField(max_length=50, blank=False, null=False, default='Put your answer here!')
    correct = models.BooleanField(default=False)

    def __unicode__(self):
        return '{1} - {2}'.format(self.id, self.value)


class Question(models.Model):
    field_of_question = models.ForeignKey(FieldOfQuestion)
    value = models.CharField(max_length=200, blank=False, null=False, default='Put you question here!')
    image = models.ImageField(upload_to='attachments', blank=True, null=True)
    answer_1 = models.ForeignKey(Answer, related_name='answer_1')
    answer_2 = models.ForeignKey(Answer, related_name='answer_2')
    answer_3 = models.ForeignKey(Answer, related_name='answer_3')
    answer_4 = models.ForeignKey(Answer, related_name='answer_4')

    def __unicode__(self):
        return '{1} - {2}'.format(self.field_of_question, self.value)