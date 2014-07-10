import codecs
import os
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from mgr.models import Department, FieldOfStudy, FieldOfQuestion, Question, Answer


@login_required
def main_page(request):
    return render_to_response('main_page.html', {}, RequestContext(request))


@login_required()
def all_questions(request):
    return render_to_response('mgr/all_questions.html', {}, RequestContext(request))


@login_required()
def choose_department(request):
    if request.POST:
        return redirect('showfieldofquestions/%s' % (request.POST.get('kierunek')))

    departments = Department.objects.all()
    field_of_study = FieldOfStudy.objects.all()
    return render_to_response('mgr/choose_department.html', {
        'departments': departments,
        'field_of_study': field_of_study
    }, RequestContext(request))


@login_required()
def show_field_of_questions(request, field_of_study_id):
    field_of_question = FieldOfQuestion.objects.filter(field_of_study__id=field_of_study_id)

    return render_to_response('mgr/field_of_question.html', {
        'field_of_question': field_of_question,
    }, RequestContext(request))


@login_required()
def work_on_questions(request):
    questions_without_answer = Question.objects.filter(approved_by_admin=False)
    count_questions = len(questions_without_answer)

    return render_to_response('mgr/work_on_questions.html', {
        'questions_without_answer': questions_without_answer,
        'count_questions': count_questions,
    }, RequestContext(request))


@login_required()
@staff_member_required
def load_questions_field_of_question(request, field_of_question_id):
    field_of_question = FieldOfQuestion.objects.get(id=field_of_question_id)
    file_path = 'media/attachments/Questions/{}.txt'.format(field_of_question.name)
    question_answer = []
    with codecs.open(file_path, encoding='utf-8') as f:
        while True:
            question = f.readline()
            answer = f.readline()
            question_answer.append((question, answer))
            if not answer:
                break  # EOF

    for number, item in enumerate(question_answer):
        if number == 0:
            pass
        else:
            print item[0], item[1]
            correct_answer, created = Answer.objects.get_or_create(value=item[1], correct=True)
            print correct_answer.id
            Question.objects.get_or_create(question_number=number, field_of_question=field_of_question,
                                           value=item[0], answer_1=correct_answer)
    pass





























