from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from django_comments.views.comments import post_comment
from django.http import HttpResponse
from django.db.models import Count

from project_share.models import Project

def comment_post_wrapper(request):
    # Clean the request to prevent form spoofing
    if request.user.is_authenticated():
        if not (request.user.get_full_name() == request.POST['name'] or \
               request.user.email == request.POST['email']):
            return HttpResponse("Error 403: You're an evil hacker")
        return post_comment(request)
    return HttpResponse("Error 403: You're an evil hacker")

def home(request):
    # Get the 10 most popular projects
    # Get the 10 newest
    projects_newest = Project.approved_projects().all().order_by('-id')[:10]
    return render_to_response('home.html', {
        "form": AuthenticationForm(),
        'projects_popular': projects_newest,
        'projects_newest': projects_newest
    }, context_instance=RequestContext(request))
