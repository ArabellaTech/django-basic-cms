"""Django page CMS functionnal tests suite module."""
from basic_cms.models import Page
from basic_cms.tests.testcase import TestCase

import json
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse


class CMSPagesApiTests(TestCase):
    maxDiff = None

    fixtures = ['pages_tests.json', 'api.json']

    # def setUp(self):
    #     self.original_data = Page.objects.from_path('terms', 'eng')
    #     self.original_json_data = json.dumps(self.original_data.dump_json_data())
    #     self.original_html_data = render_to_string(self.original_data.template,
    #                                                {"current_page": self.original_data})

    def tests_basic_cms_api_access(self):
        from django.test.client import Client
        self.client = Client()
        self.original_data = Page.objects.from_path('terms', 'en-us')
        self.original_json_data = json.dumps(self.original_data.dump_json_data())
        self.original_html_data = render_to_string(self.original_data.template,
                                                   {"current_page": self.original_data})
        data = {
            'format': 'json'
        }
        response = self.client.get(reverse('basic_cms_api', args=['alamakota']), data)
        self.assertEqual(response.status_code, 404)
        response = self.client.get(reverse('basic_cms_api', args=['terms']), data)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(json.loads(self.original_json_data), json.loads(response.content.decode("utf-8")))
        # self.assertEqual(self.original_json_data, response.content)

        response = self.client.get(reverse('basic_cms_api', args=['terms']))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Please read these Terms of Use', response.content.decode("utf-8"))

        response = self.client.get(reverse('basic_cms_api', args=['coaches']), {'format': 'json'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title']['en-us'], 'coaches')
        self.assertEqual(len(response.data['children']), 3)
        self.assertEqual(response.data['children'][0]['title']['en-us'], 'Judith Singer')
        self.assertEqual(response.data['children'][1]['title']['en-us'], 'Melissa Litwak')
        self.assertEqual(response.data['children'][2]['title']['en-us'], 'Joanna Schaffler')

    def test_urls(self):
        from utils import links_append_domain

        body = """<a href="http://google.com">google.com</a><a href="foo">foo</a><a href="#a">#a</a><a href="/#a">/#a</a><img src="http://x.com/x.jpg"/><img src="a.jpg"/>
        """
        return_body = """<html><body><a href="http://google.com">google.com</a><a href="http://a.com/foo">foo</a><a href="#a">#a</a><a href="/#a">/#a</a><img src="http://x.com/x.jpg"/><img src="http://a.com/a.jpg"/></body></html>
        """
        self.assertEqual(links_append_domain(body, 'http://a.com').strip(), return_body.strip())
