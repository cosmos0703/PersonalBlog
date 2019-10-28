from tests.testbase import Testbase
from shared.storage.base_table import BaseTable
from azure.storage import table


class TestBaseTable(Testbase):
    def test_table_creation(self):
        name = 'TestCreationTable'
        t = BaseTable(name)
        self.assertFalse(t._service.exists(name))
        t.create_table()
        self.assertTrue(t._service.exists(name))
        t._service.delete_table(name)

    def test_table_deletion(self):
        name = 'TestDeletionTable'
        t = BaseTable(name)
        t._service.create_table(name)
        self.assertTrue(t._service.exists(name))
        t.delete_table()
        self.assertFalse(t._service.exists(name))
