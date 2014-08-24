import codecs
import random
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from mgr.forms import QuestionForm
from mgr.models import Department, FieldOfStudy, FieldOfQuestion, Question, Answer, UserProfile


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
def show_field_of_question(request, field_of_study_id):
    field_of_question = FieldOfQuestion.objects.filter(field_of_study__id=field_of_study_id)

    return render_to_response('mgr/field_of_question.html', {
        'field_of_question': field_of_question,
    }, RequestContext(request))


@login_required()
def work_on_question(request):
    questions_without_answer = Question.objects.filter(approved_by_admin=False, is_prepared=False)
    questions_to_do_id = [question_id.id for question_id in questions_without_answer]
    random_id = random.choice(questions_to_do_id)
    random_question = Question.objects.get(id=random_id)
    user = UserProfile.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = QuestionForm(instance=random_question, data=request.POST)
        if form.is_valid():
            print request.POST
            answer_2, created = Answer.objects.get_or_create(value=request.POST.get('answer_B'))
            answer_3, created = Answer.objects.get_or_create(value=request.POST.get('answer_C'))
            answer_4, created = Answer.objects.get_or_create(value=request.POST.get('answer_D'))
            obj = form.save(commit=False)
            obj.answer_2 = answer_2
            obj.answer_3 = answer_3
            obj.answer_4 = answer_4
            user.question_prepared.add(obj)
            obj.is_prepared = True
            obj.save()
    else:
        form = QuestionForm(instance=random_question)
    questions_done = user.question_prepared.count()
    print questions_done
    return render_to_response('mgr/work_on_questions.html', {
        'questions_without_answer': questions_without_answer,
        'count_questions': len(questions_to_do_id),
        'form': form,
        'question': random_question,
        'questions_done': questions_done,
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
            question_answer.append((question, answer[:-1]))
            if not answer:
                break  # EOF

    for number, item in enumerate(question_answer):
        if item[0]:
            correct_answer, created = Answer.objects.get_or_create(value=item[1], correct=True)
            Question.objects.get_or_create(question_number=number+1, field_of_question=field_of_question, value=item[0], answer_1=correct_answer)
    pass





























