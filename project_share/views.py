from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy

from taggit.models import Tag

from extra_views import SortableListMixin
from extra_views import SearchableListMixin

from project_share.models import Application, Project, ApplicationDemo, Classroom, Approval, Address
from project_share.forms import ProjectForm, ApprovalForm, AddressForm

try:
    from django.contrib.auth import get_user_model
except ImportError: # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()

class RestrictPermissionMixin(object):
    def dispatch(self, request, *args, **kwargs):
        self.kwargs = kwargs
        self.request = request
        return super(RestrictPermissionMixin, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        o = super(RestrictPermissionMixin, self).get_object()

        # If the object doesn't belong to this user and isn't published, throw a error 503
        if ((not o.approved and o.owner != self.request.user) or o.approval != None) and not self.request.user.is_superuser:
            raise PermissionDenied()
        return o

class ApplicationList(ListView):
    model = Application

class ApplicationDetail(DetailView):
    model = Application

class ApplicationRunDetail(DetailView):
    model = Application
    context_object_name = 'application'
    template_name = "project_share/application_csnap.html"

    def render_to_response(self, context, **response_kwargs):
        app = Application.objects.get(pk=self.kwargs['pk'])
        unique_modules = []
        if(app.module):
            module_list = app.module.get_modules()
            [unique_modules.append(module) for module in module_list if module not in unique_modules]
        context['modules'] = unique_modules
        return super(ApplicationRunDetail, self).render_to_response(context, **response_kwargs)

class ProjectList(SearchableListMixin, SortableListMixin, ListView):
    sort_fields_aliases = [('name', 'by_name'), ('id', 'by_id'), ('votes', 'by_likes'), ]
    search_fields = [('application__name','iexact')]
    search_split = False
    model = Project
    queryset = Project.objects.all()

    def render_to_response(self, context, **response_kwargs):
        proj = Project.objects.get(pk=self.kwargs['pk'])
        unique_modules = []
        if(proj.application.module):
            module_list = proj.application.module.get_modules()
            [unique_modules.append(module) for module in module_list if module not in unique_modules]
        context['modules'] = unique_modules
        context['application_list'] = Application.objects.all()
        return super(ProjectList, self).render_to_response(context, **response_kwargs)

class ProjectTagList(ProjectList):
    def get_queryset(self):
        self.tag = get_object_or_404(Tag, pk=self.kwargs['tag_pk'])
        return Project.approved_objects.filter(tags__in=[self.tag])

class ProjectDetail(RestrictPermissionMixin, DetailView):
    model = Project

class ProjectRunDetail(RestrictPermissionMixin, DetailView):
    model = Project
    template_name = "project_share/application_csnap.html"
    context_object_name = 'project'

    def render_to_response(self, context, **response_kwargs):
        context['application'] = context['project'].application
        return super(ProjectRunDetail, self).render_to_response(context, **response_kwargs)

class ProjectPresentDetail(ProjectRunDetail):
    def render_to_response(self, context, **response_kwargs):
        context['present'] = True
        return super(ProjectPresentDetail, self).render_to_response(context, **response_kwargs)

class ProjectCreate(CreateView):
    model = Project
    form_class = ProjectForm

    def get_success_url(self):
        return reverse('project-update', kwargs={'pk': self.object.id})

    def dispatch(self, request, *args, **kwargs):
        self.kwargs = kwargs
        self.request = request
        return super(ProjectCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(ProjectCreate, self).form_valid(form)

class ProjectUpdate(UpdateView):
    model = Project
    form_class = ProjectForm

    template_name = "project_share/project_edit.html"


    def dispatch(self, request, *args, **kwargs):
        self.kwargs = kwargs
        self.request = request
        return super(ProjectUpdate, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        o = super(ProjectUpdate, self).get_object()

        # If the object doesn't belong to this user, throw a error 503
        if o.owner != self.request.user or o.approval != None:
            raise PermissionDenied()
        return o

class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('project-delete-success')

class DemoList(ListView):
    model = ApplicationDemo

class DemoDetail(DetailView):
    model = ApplicationDemo

class ApprovalCreate(CreateView):
    model = Approval
    form_class = ApprovalForm

    def dispatch(self, request, *args, **kwargs):
      self.kwargs = kwargs
      self.request = request
      return super(ApprovalCreate, self).dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        form.instance.project_id = self.kwargs['project_pk']
        return super(ApprovalCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('approval-confirm')


class UserDetail(DetailView):
    model = User
    template_name = "project_share/user_detail.html"

class AddressCreate(CreateView):
    model = Address
    form_class = AddressForm

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        return super(AddressCreate, self).form_valid(form)

    def get_success_url(self):
        return u'/'

class AddressUpdate(UpdateView):
    model = Address
    form_class = AddressForm

    template_name = "project_share/address_form.html"

    def dispatch(self, request, *args, **kwargs):
      if(not request.user.id == int(self.kwargs['pk'])):
         raise PermissionDenied
      return super(AddressUpdate, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('address-confirm')
