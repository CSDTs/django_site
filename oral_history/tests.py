# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Interview, OralHistory
from .forms import OHPForm, TagForm
from project_share.models import Project, Application

# Create your tests here.


class InterviewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user('test-user')
        ohp = OralHistory.objects.create(project_name="Test OHP", byline="OHP Byline",
                                         summary="OHP Summary", slug="test-ohp", is_official=True, approved=True)
        app = Application.objects.create(name="test_app", application_type="OHP")
        csdt = Project.objects.create(name="csdt_proj", application=app)
        self.interview = Interview.objects.create(project=ohp,
                                                  full_name="John Doe",
                                                  date="Nov 20, 2018",
                                                  location="Troy, NY",
                                                  interview_by="Jane Doe",
                                                  birthplace="Anytown, USA",
                                                  occupation="Worker",
                                                  birth_year="1960",
                                                  slug="john-doe",
                                                  approved=True,
                                                  csdt_project=csdt)

    def test_ohp_views(self):
        url = '/oralhistory/test-ohp/'
        response = self.client.get(url, **{'HTTP_REFERER': url})
        self.assertTrue(response.status_code == 300 or response.status_code == 200,
                        msg="Got code %s on %s" % (response.status_code, url))
        url = '/oralhistory/test-ohp/john-doe'
        response = self.client.get(url, **{'HTTP_REFERER': url})
        self.assertTrue(response.status_code == 300 or response.status_code == 200,
                        msg="Got code %s on %s" % (response.status_code, url))

    def test_interview_form(self):
        form = OHPForm({'user': self.user, 'is_official': False, 'approved': True, 'project_name': 'test-OHP',
                        'byline': 'new oralhistory project', 'summary': 'ohp summary', 'slug': 'test-ohp'})
        self.assertTrue(form.is_valid())
        ohp_form = form.save()
        self.assertEqual(ohp_form.summary, 'ohp summary')
        self.assertEqual(ohp_form.byline, 'new oralhistory project')
        self.assertEqual(ohp_form.slug, 'test-ohp')
        self.assertEqual(ohp_form.project_name, 'test-OHP')
        self.assertEqual(ohp_form.approved, True)
        self.assertEqual(ohp_form.is_official, False)
        self.assertEqual(ohp_form.user, self.user)

    def test_tag_form(self):
        form = TagForm({'timestamp': 45, 'tag': 'talks about the city', 'interview': self.interview, 'approved': True})
        self.assertTrue(form.is_valid())
        tag_form = form.save()
        self.assertEqual(tag_form.tag, 'talks about the city')
        self.assertEqual(tag_form.timestamp, 45)
        self.assertEqual(tag_form.interview, self.interview)
        self.assertEqual(tag_form.approved, True)