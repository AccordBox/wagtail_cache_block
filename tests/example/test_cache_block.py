"""
./manage.py dumpdata --natural-foreign --indent 2 \
    -e contenttypes -e auth.permission \
    -e wagtailcore.groupcollectionpermission \
    -e wagtailcore.grouppagepermission -e wagtailimages.rendition \
    -e sessions > data.json
"""

from django.core.cache import cache
from django.test import TestCase, override_settings
from tests.example.models import ArticlePage
from django.test import Client
from django.core import management

from django.db import connection


class TestCacheBlock(TestCase):
    fixtures = ['data.json']

    def cache_count(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(ALL) from my_cache_table")
            row = cursor.fetchone()
        return row

    def setUp(self):
        management.call_command('createcachetable', verbosity=0)
        cache.clear()

    def test_char_field(self):
        page = ArticlePage.objects.get(pk=5)
        client = Client()

        response = client.get(page.url)
        self.assertEqual(response.status_code, 200)

        count = self.cache_count()

        new_value = 'this is a good start'
        page.body.stream_data[0]['value'] = new_value
        page.save_revision().publish()

        response = client.get(page.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(new_value, response.content.decode('utf-8'))

        new_count = self.cache_count()

        self.assertNotEquals(count, new_count)

    def test_struct_block(self):
        page = ArticlePage.objects.get(pk=5)
        client = Client()

        response = client.get(page.url)
        self.assertEqual(response.status_code, 200)

        count = self.cache_count()

        # change it to another page pk
        page.body.stream_data[3]['value']['reference_page'] = 4
        page.save_revision().publish()

        response = client.get(page.url)
        self.assertEqual(response.status_code, 200)

        new_count = self.cache_count()

        self.assertNotEquals(count, new_count)

    def test_stream_block(self):
        page = ArticlePage.objects.get(pk=5)
        client = Client()

        response = client.get(page.url)
        self.assertEqual(response.status_code, 200)

        count = self.cache_count()

        # change it to another page pk
        page.body.stream_data[4]['value'][1]['value']['reference_page'] = 3
        page.save_revision().publish()

        response = client.get(page.url)
        self.assertEqual(response.status_code, 200)

        new_count = self.cache_count()

        self.assertNotEquals(count, new_count)

    def test_column_struct_data(self):
        page = ArticlePage.objects.get(pk=5)
        client = Client()

        response = client.get(page.url)
        self.assertEqual(response.status_code, 200)

        count = self.cache_count()

        # change it to another page pk
        page.body.stream_data[5]['value']['reference_page'] = 4
        page.save_revision().publish()

        response = client.get(page.url)
        self.assertEqual(response.status_code, 200)

        new_count = self.cache_count()

        self.assertNotEquals(count, new_count)

    def test_column_stream_data(self):
        page = ArticlePage.objects.get(pk=5)
        client = Client()

        response = client.get(page.url)
        self.assertEqual(response.status_code, 200)

        count = self.cache_count()

        # change it to another page pk
        page.body.stream_data[6]['value'][1]['value']['reference_page'] = 3
        page.save_revision().publish()

        response = client.get(page.url)
        self.assertEqual(response.status_code, 200)

        new_count = self.cache_count()

        self.assertNotEquals(count, new_count)
