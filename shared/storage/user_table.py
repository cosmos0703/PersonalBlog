import os
from datetime import datetime
from azure.common import AzureMissingResourceHttpError
from .base_table import BaseTable

class UserTable(BaseTable):
    DefaultTableName = 'PristineUserTable'
    DefaultPartitionKey = 'User'

    def __init__(self, table_name: str = None):
        super().__init__(table_name or UserTable.DefaultTableName)

    def add_user(self, email: str, passwordhash: str):
        task = {
            'PartitionKey': UserTable.DefaultPartitionKey,
            'RowKey': email,
            'Email': email,
            'PasswordHash': passwordhash,
            'CreatedUtc': datetime.utcnow().isoformat(),
            'LastLoginUtc': None
        }
        self._service.insert_entity(self._table_name, task)

    def remove_user(self, email: str):
        self._service.delete_entity(self._table_name, UserTable.DefaultPartitionKey, email)

    def get_user(self, email: str):
        try:
            return self._service.get_entity(self._table_name, UserTable.DefaultPartitionKey, email)
        except AzureMissingResourceHttpError:
            return None
