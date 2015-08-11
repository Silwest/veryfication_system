import codecs
import random
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from mgr.forms import QuestionForm
from mgr.models import Department, FieldOfStudy, FieldOfQuestion, Question, Answer, UserProfile, CustomTest, Statistic
from django.contrib import messages


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
    custom_test = CustomTest.objects.filter(approved_by_admin=True)
    questions_for_field = []
    color_list = ['#98df8a', '#d62728', '#ffbb78']  # opracowane, nieopracowane, przygotowane
    chart_type = "pieChart"
    extra_series = {"tooltip": {"y_start": "", "y_end": " pytan"}, 'color': '#FF8aF8'}

    for question_field in field_of_question:
        questions = Question.objects.filter(field_of_question=question_field)
        questions_approved = len(questions.filter(approved_by_admin=True))
        questions_prepared = len(questions.filter(is_prepared=True, approved_by_admin=False))
        questions_not_ready = len(questions.filter(is_prepared=False, approved_by_admin=False))
        dictionary = {
            'field_of_study': question_field.name,
            'questions_not_ready': questions_not_ready,
            'questions_approved': questions_approved,
            'questions_prepared': questions_prepared,
            }
        questions_for_field.append(dictionary)
    questions_approved = len(Question.objects.filter(field_of_question__in=field_of_question, approved_by_admin=True))
    questions_not_ready = len(Question.objects.filter(field_of_question__in=field_of_question, is_prepared=False, approved_by_admin=False))
    questions_prepared = len(Question.objects.filter(field_of_question__in=field_of_question, is_prepared=True, approved_by_admin=False))
    x_data = ['Opracowane', 'Nieopracowane', 'Przygotowane']
    y_data = [[questions_approved, questions_not_ready, questions_prepared]]
    for item in questions_for_field:
        y_data.append(item.values()[1:])
    # add questions from custom test
    chart_data = []
    for test in custom_test:
        chart_data.append({'x': x_data, 'y': [len(test.questions.all()), 0, 0], 'extra': extra_series})
    # for number, item in enumerate(custom_test):
    #     chart_data.append({'x': x_data, 'y': y_data[number], 'extra': extra_series})
    print chart_data
    # chart_data_custom = {'x': x_data, 'y': chart_data[0], 'extra': extra_series}
    chart_data_0 = {'x': x_data, 'y': y_data[0], 'extra': extra_series}
    chart_data_1 = {'x': x_data, 'y': y_data[1], 'extra': extra_series}
    chart_data_2 = {'x': x_data, 'y': y_data[2], 'extra': extra_series}
    chart_data_3 = {'x': x_data, 'y': y_data[3], 'extra': extra_series}
    print chart_data
    # print chart_data_custom
    data = {
        'chart_type': chart_type,
        'chart_data': chart_data,
        'chart_data_0': chart_data_0,
        'chart_data_1': chart_data_1,
        'chart_data_2': chart_data_2,
        'chart_data_3': chart_data_3,
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
    else:
        form = random_question = None
    questions_done = user.question_prepared.count()
    return render_to_response('mgr/work_on_questions.html', {
        'questions_without_answer': questions_without_answer,
        'count_questions': len(questions_to_do_id),
        'form': form,
        'question': random_question,
        'questions_done': questions_done,
    }, RequestContext(request))


@login_required()
def save_question(request, question_id, accept=False):
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
            if accept == "True":
                obj.approved_by_admin = True
            obj.save()
            if accept == "False":
                user.question_prepared.add(obj)
                return redirect('/workonquestion')
            return redirect('/acceptquestion')


@login_required()
@staff_member_required
def accept_question(request):
    answered_questions = Question.objects.filter(approved_by_admin=False, is_prepared=True)
    questions_to_do_id = [question_id.id for question_id in answered_questions]
    if questions_to_do_id:
        random_question_id = random.choice(questions_to_do_id)
        random_question = Question.objects.get(id=random_question_id)
        form = QuestionForm(instance=random_question)
    else:
        form = random_question = None
    return render_to_response('admin/accept_question.html',
                              {
                                  'form': form,
                                  'question': random_question,
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
            Question.objects.get_or_create(question_number=number + 1, field_of_question=field_of_question, value=item[0], answer_1=correct_answer)
    pass


@login_required()
def start_test(request, field_of_question="all"):
    if field_of_question == "all":
        question_approved = Question.objects.filter(approved_by_admin=True).order_by('id')
    elif field_of_question == "custom":
        custom_test = CustomTest.objects.get(name__icontains="Silwest")
        question_approved = custom_test.questions.all()
    else:
        question_approved = Question.objects.filter(field_of_question__name__icontains=field_of_question, approved_by_admin=True)
    return render_to_response('mgr/start_test.html', {
        'question_approved': question_approved,
    }, RequestContext(request))


@login_required()
def check_answers(request):
    answers = []
    correct_answers = 0
    for item in request.POST:
        if '-' in request.POST.get(item):
            question_id, answer_id = request.POST.get(item).split('-')
            answers.append(check_correct_answer(request.user, question_id, answer_id))
    for value in answers:
        if value is True:
            correct_answers += 1

    return redirect('display_results', answers=len(answers), correct_answers=correct_answers)


def display_results(request, answers, correct_answers):
    color_list = ['#98df8a', '#d62728', '#ffbb78']  # opracowane, nieopracowane, przygotowane
    chart_type = "pieChart"
    x_data = ['Dobrze', 'Zle']
    y_data = [correct_answers, int(answers)-int(correct_answers)]
    extra_series = {"tooltip": {"y_start": "", "y_end": " pytan"}, 'color': '#FF8aF8'}

    chart_data_0 = {'x': x_data, 'y': y_data, 'extra': extra_series}
    data = {
        'chart_type': chart_type,
        'chart_data_0': chart_data_0,
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
    return render_to_response('mgr/display_results.html', data, RequestContext(request))


def check_correct_answer(user, question_id, answer_id):
    question = Question.objects.get(id=question_id)
    answer = Answer.objects.get(id=answer_id)
    if answer.correct is True:
        answer_correct(user, question.field_of_question)
        return True
    else:
        answer_incorrect(user, question.field_of_question)
        return False


def answer_correct(user, field_of_question):
    user_stats, created = Statistic.objects.get_or_create(user=user, field_of_question=field_of_question)
    user_stats.correct_answers += 1
    user_stats.all_answers += 1
    user_stats.save()


def answer_incorrect(user, field_of_question):
    user_stats, created = Statistic.objects.get_or_create(user=user, field_of_question=field_of_question)
    user_stats.all_answers += 1
    user_stats.save()


def statistics(request):
    print request.user

    pass


@login_required()
def create_test(request):
    if request.POST:
        name_of_test = request.user.get_full_name() + " test"
        custom_test, created = CustomTest.objects.get_or_create(name=name_of_test)
        for item in request.POST:
            if item != 'csrfmiddlewaretoken':
                question = Question.objects.get(id=item)
                custom_test.questions.add(question)
                custom_test.save()
        messages.add_message(request, messages.SUCCESS, "Custom Test has been created.")
    question_approved = Question.objects.filter(approved_by_admin=True).order_by('id')
    return render_to_response('mgr/create_test.html', {
            'question_approved': question_approved,
            }, RequestContext(request))