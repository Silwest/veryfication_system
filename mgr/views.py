from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext


@login_required
def main_page(request):
    return render_to_response('main_page.html', {}, RequestContext(request))

@login_required()
def all_questions(request):
    return render_to_response('mgr/all_questions.html', {}, RequestContext(request))