from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import ModelForm, HiddenInput
from mgr.models import Question, CustomTest


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
        widgets = {
            'question_number': HiddenInput(),
            'value': HiddenInput(),
            'is_prepared': HiddenInput(),
            'answer_1': HiddenInput(),
            'answer_2': HiddenInput(),
            'answer_3': HiddenInput(),
            'answer_4': HiddenInput(),
            'field_of_question': HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        # self.fields['image'].widget = HiddenInput()
        self.fields['approved_by_admin'].widget = HiddenInput()
        self.fields['question_number'].widget.attrs.update({'readonly': 'True'})
        self.fields['value'].widget.attrs.update({'readonly': 'True'})
        self.fields['field_of_question'].widget.attrs.update({'readonly': 'True'})
        self.fields['answer_1'].widget.attrs.update({'readonly': 'True'})
        self.is_prepared = True

        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'form-control'})


class CustomTestForm(ModelForm):
    questions = forms.ModelMultipleChoiceField(Question.objects.all(),
                                               widget=FilteredSelectMultiple('Questions', False, attrs={'rows': 10}))

    class Meta:
        fields = '__all__'
        model = CustomTest