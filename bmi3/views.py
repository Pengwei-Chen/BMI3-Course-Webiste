from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.conf import settings
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.static import serve
from .ag import parse_ag_result, execute_ag
import os
import json


PRACTICAL_BREADCRUMBS = {
    0: ["<a href='../../'>Home</a>", "<a>Start up</a>"],
    1: ["<a href='../../'>Home</a>", "<a>Practical 1: sorting </a>"]
}


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

def course_handbook(request):
    return serve(request, "", os.path.join(settings.BASE_DIR, "static/pdf", "2022CouseHandbook_BMI3_Finalv3.pdf"))
    # return download(request, "2022CouseHandbook_BMI3_Finalv2.pdf")

# def practical(request, practical_id):
#     if not request.user.is_authenticated:
#         return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
#     template = loader.get_template('practical-template.html')
#     with open(os.path.join(settings.PRACTICAL_DIR, "{}.txt".format(practical_id))) as f:
#         s = "".join(f.readlines())
#     return HttpResponse(template.render({
#         "breadcrumbs": PRACTICAL_BREADCRUMBS[practical_id],
#         "main": s
#     }, request))


def calendar(request):
    template = loader.get_template('calendar.html')
    return HttpResponse(template.render({}, request))

def textbooks(request):
    # if not request.user.is_authenticated:
    #     return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    template = loader.get_template('textbooks.html')
    return HttpResponse(template.render({}, request))

def team(request):
    template = loader.get_template('team.html')
    return HttpResponse(template.render({}, request))

def download(request, pdf):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    return serve(request, "", os.path.join(settings.BASE_DIR, "static/pdf", pdf))

@csrf_exempt
def api(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = json.loads(request.body)
        if form["type"] == "ag":
            result = parse_ag_result(execute_ag(settings.TEMPLATES_DIR, form["pattern"]))
            print(list(map(lambda x: [PRACTICAL_BREADCRUMBS[int(x[0].split(".")[0])],dict(x[1])], result)))
            result = dict(list(map(lambda x: [PRACTICAL_BREADCRUMBS[int(x[0].split(".")[0])][-1],dict(x[1])], result)))
            return JsonResponse(result)
        else:
            return JsonResponse({"error":"unknown request type"})
    else:
        return JsonResponse({"error":"unknown request type"})