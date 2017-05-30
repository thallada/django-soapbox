from django import template
from django.test import TestCase


class TagTests(TestCase):
    fixtures = ['soapboxtest.json']

    def test_success_root(self):
        """
        Test retrieval on the root URL, which should retrieve only a
        global Message.

        """
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            len(r.context['soapbox_messages']), 1)
        self.assertContains(
            r, "This is a global message.")

    def test_success_with_match(self):
        """
        Test retrieval on a URL which will have a global Message and a
        Message with an exact URL match.

        """
        r = self.client.get('/foo/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            len(r.context['soapbox_messages']), 3)
        self.assertContains(
            r, "This is a global message.")
        self.assertContains(
            r, "This message appears on /foo/ and on /foo/bar/.")

    def test_success_with_multiple_match(self):
        """
        Test retrieval on a URL which will have a global Message, an
        exact URL match and a prefix URL match.

        """
        r = self.client.get('/foo/bar/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            len(r.context['soapbox_messages']), 6)
        self.assertContains(
            r, "This is a global message.")
        self.assertContains(
            r, "This message appears on /foo/ and on /foo/bar/.")
        self.assertContains(
            r, "This message appears only on /foo/bar/.")

    def test_html(self):
        """
        Test that HTML in Messages is passed through unescaped.

        """
        r = self.client.get('/foo/bar/')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, '<a href="/foo/bar/">')

    def test_fail_syntax(self):
        """
        Test that incorrect tag syntax raises TemplateSyntaxError.

        """
        self.assertRaises(
            template.TemplateSyntaxError,
            self.client.get,
            '/fail/')

    def test_bad_url_var(self):
        """
        Test that a bad URL variable passed to the tag bails out with
        no results.

        """
        r = self.client.get('/bad-url-var/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual([], r.context['soapbox_messages'])
