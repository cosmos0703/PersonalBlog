from datetime import datetime
from tests.testbase import Testbase
from shared.storage import UserTable
from azure.storage import table


class TestUserTable(Testbase):
    TestTableName = 'TestUserTable' + datetime.utcnow().strftime('%H%M%S')

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        service = table.TableService(connection_string=cls._azure_webjobs_storage)
        service.create_table(cls.TestTableName)

    @classmethod
    def tearDownClass(cls):
        s  = table.TableService(connection_string=cls._azure_webjobs_storage)
        s.delete_table(cls.TestTableName)

    def test_add_user(self):
        email = 'insert@pristine.com'
        password_hash = 'passwordhash'
        t = UserTable(TestUserTable.TestTableName)
        t.add_user(email, password_hash)
        entity = t.get_user(email)
        self.assertEqual(entity.get('Email'), email)
        self.assertEqual(entity.get('PasswordHash'), password_hash)
        self.assertIsNotNone(entity.get('CreatedUtc'))

    def test_remove_user(self):
        email = 'removal@pristine.com'
        password_hash = 'passwordhash'
        t = UserTable(TestUserTable.TestTableName)
        t.add_user(email, password_hash)
        t.remove_user(email)
        entity = t.get_user(email)
        self.assertIsNone(entity)
