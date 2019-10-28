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

    def test_list_blogs_by_author(self):
        email = 'email@pristine.com'
        title = 'test_list_blogs_by_author'
        text = 'test_list_blogs_by_author'
        t = BlogTable(TestBlogTable.TestTableName)
        t.add_blog(email, title, text)
        titles = t.list_blogs_by_author(email)
        self.assertIn(title, titles)

    def test_list_blogs_by_separated_author(self):
        content = {
            "userA": {
                'email': 'email_a@pristine.com',
                'title': 'test_list_blogs_by_separated_author_a',
                'text': 'test_list_blogs_by_separated_author_a'
            },
            "userB": {
                'email': 'email_b@pristine.com',
                'title': 'test_list_blogs_by_separated_author_b',
                'text': 'test_list_blogs_by_separated_author_b'
            }
        }
        t = BlogTable(TestBlogTable.TestTableName)
        t.add_blog(**content['userA'])
        t.add_blog(**content['userB'])
        titles = t.list_blogs_by_author(content['userA']['email'])
        self.assertIn(content['userA']['title'], titles)
        self.assertNotIn(content['userB']['title'], titles)

    def test_list_all_blogs(self):
        content = {
            "userA": {
                'email': 'email_a@pristine.com',
                'title': 'test_list_all_blogs_a',
                'text': 'test_list_all_blogs_a'
            },
            "userB": {
                'email': 'email_b@pristine.com',
                'title': 'test_list_all_blogs_b',
                'text': 'test_list_all_blogs_b'
            }
        }
        t = BlogTable(TestBlogTable.TestTableName)
        t.add_blog(**content['userA'])
        t.add_blog(**content['userB'])
        titles = t.list_blogs()
        self.assertIn(content['userA']['title'], titles)
        self.assertIn(content['userB']['title'], titles)
