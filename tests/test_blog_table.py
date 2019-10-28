import json
from datetime import datetime
from tests.testbase import Testbase
from shared.storage import BlogTable
from azure.storage import table


class TestBlogTable(Testbase):
    TestTableName = 'TestBlogTable' + datetime.utcnow().strftime('%H%M%S')

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        service = table.TableService(connection_string=cls._azure_webjobs_storage)
        service.create_table(cls.TestTableName)

    @classmethod
    def tearDownClass(cls):
        s  = table.TableService(connection_string=cls._azure_webjobs_storage)
        s.delete_table(cls.TestTableName)

    def test_insert_blog(self):
        email = 'email@pristine.com'
        title = 'test_insert_blog'
        text = 'test_insert_blog'
        t = BlogTable(TestBlogTable.TestTableName)
        t.add_blog(email, title, text)
        entity = t.get_blog(email, title)
        self.assertEqual(entity.get('Author'), email)
        self.assertEqual(entity.get('Title'), title)
        self.assertEqual(entity.get('Text'), text)
        self.assertIsNotNone(entity.get('CreatedUtc'))

    def test_remove_blog(self):
        email = 'email@pristine.com'
        title = 'test_remove_blog'
        text = 'test_remove_blog'
        t = BlogTable(TestBlogTable.TestTableName)
        t.add_blog(email, title, text)
        t.remove_blog(email, title)
        entity = t.get_blog(email, title)
        self.assertIsNone(entity)

    def test_add_tag_to_blog(self):
        email = 'email@pristine.com'
        title = 'test_add_tag_to_blog'
        text = 'test_add_tag_to_blog'
        t = BlogTable(TestBlogTable.TestTableName)
        t.add_blog(email, title, text)
        t.add_tag(email, title, 'tag')
        entity = t.get_blog(email, title)
        self.assertEqual(entity.get('Tags'), json.dumps(['tag']))

    def test_remove_tag_from_blog(self):
        email = 'email@pristine.com'
        title = 'test_remove_tag_from_blog'
        text = 'test_remove_tag_from_blog'
        t = BlogTable(TestBlogTable.TestTableName)
        t.add_blog(email, title, text)
        t.add_tag(email, title, 'tag')
        entity = t.get_blog(email, title)
        self.assertEqual(entity.get('Tags'), json.dumps(['tag']))

        t.remove_tag(email, title, 'tag')
        entity = t.get_blog(email, title)
        self.assertEqual(entity.get('Tags'), json.dumps([]))
