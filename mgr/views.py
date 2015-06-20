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
        return redirect('mgr.views.show_field_of_question', request.POST.get('kierunek'))

    departments = Department.objects.all()
    field_of_study = FieldOfStudy.objects.all()
    return render_to_response('mgr/choose_department.html', {
        'departments': departments,
        'field_of_study': field_of_study
    }, RequestContext(request))


@login_required()
def show_field_of_question(request, field_of_study_id):
    field_of_question = FieldOfQuestion.objects.filter(field_of_study__id=field_of_study_id)
    questions_for_field = []
    for question_field in field_of_question:
        questions = Question.objects.filter(field_of_question=question_field)
        questions_approved = len(questions.filter(approved_by_admin=True))
        questions_prepared = len(questions.filter(is_prepared=True))
        questions_not_ready = len(questions.filter(is_prepared=False, approved_by_admin=False))
        dictionary = {
            'field_of_study': question_field.name,
            'questions_not_ready': questions_not_ready,
            'questions_approved': questions_approved,
            'questions_prepared': questions_prepared,
        }
        questions_for_field.append(dictionary)
    print questions_for_field
    x_data = ['Opracowane', 'Nieopracowane', 'Przygotowane']
    y_data = []
    for item in questions_for_field:
        print item.values
        y_data.append(item.values()[1:])
    color_list = ['#98df8a', '#d62728', '#ffbb78']  #opracowane, nieopracowane, przygotowane
    chart_type = "pieChart"
    extra_series = {"tooltip": {"y_start": "", "y_end": " pytan"}, 'color': '#FF8aF8'}
    chart_data_0 = {'x': x_data, 'y': y_data[0], 'extra': extra_series}
    chart_data_1 = {'x': x_data, 'y': y_data[1], 'extra': extra_series}
    chart_data_2 = {'x': x_data, 'y': y_data[2], 'extra': extra_series}
    data = {
        'chart_type': chart_type,
        'chart_data_0': chart_data_0,
        'chart_data_1': chart_data_1,
        'chart_data_2': chart_data_2,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
            'chart_attr': {'color': color_list, 'labelType': '"percent"'},
            'donut': True,
            # 'showLabels': True,
        },
    }
    return render_to_response('mgr/field_of_question.html', data, RequestContext(request))


@login_required()
def work_on_question(request):
    user = UserProfile.objects.get(id=request.user.id)
    questions_without_answer = Question.objects.filter(approved_by_admin=False, is_prepared=False)
    questions_to_do_id = [question_id.id for question_id in questions_without_answer]
    if questions_to_do_id:
        random_id = random.choice(questions_to_do_id)
        random_question = Question.objects.get(id=random_id)
        form = QuestionForm(instance=random_question)
    questions_done = user.question_prepared.count()
    form = random_question = None
    return render_to_response('mgr/work_on_questions.html', {
        'questions_without_answer': questions_without_answer,
        'count_questions': len(questions_to_do_id),
        'form': form,
        'question': random_question,
        'questions_done': questions_done,
    }, RequestContext(request))


@login_required()
def save_question(request, question_id):
    user = UserProfile.objects.get(id=request.user.id)
    question = Question.objects.get(id=question_id)

    if request.method == 'POST':
        form = QuestionForm(instance=question, data=request.POST)
        if form.is_valid():
            answer_2, created = Answer.objects.get_or_create(value=request.POST.get('answer_B'))
            answer_3, created = Answer.objects.get_or_create(value=request.POST.get('answer_C'))
            answer_4, created = Answer.objects.get_or_create(value=request.POST.get('answer_D'))
            obj = form.save(commit=False)
            obj.answer_2 = answer_2
            obj.answer_3 = answer_3
            obj.answer_4 = answer_4
            obj.is_prepared = True
            obj.save()
            user.question_prepared.add(obj)
            return redirect('/workonquestion')


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
            Question.objects.get_or_create(question_number=number + 1, field_of_question=field_of_question, value=item[0], answer_1=correct_answer)
    pass
