import os
from azure.storage import table
from .base_storage import BaseStorage

class BaseTable(BaseStorage):
    def __init__(self, table_name: str):
        super().__init__()
        self._service = table.TableService(connection_string=self._connection_string)
        self._table_name = table_name

    def create_table(self):
        self._service.create_table(self._table_name)

    def exist_table(self) -> bool:
        return self._service.exists(self._table_name)

    def delete_table(self):
        self._service.delete_table(self._table_name)
