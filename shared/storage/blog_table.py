from typing import Set
import os
import json
from datetime import datetime
from azure.common import AzureMissingResourceHttpError
from .base_table import BaseTable

class BlogTable(BaseTable):
    DefaultTableName = 'PristineBlogTable'

    def __init__(self, table_name: str = None):
        super().__init__(table_name or BlogTable.DefaultTableName)

    def add_blog(self, email: str, title: str, text: str):
        task = {
            'PartitionKey': email,
            'RowKey': title,
            'Author': email,
            'Title': title,
            'Text': text,
            'Tags': '[]',
            'CreatedUtc': datetime.utcnow().isoformat(),
            'RemovalUtc': None,
            'LastModifiedUtc': datetime.utcnow().isoformat(),
        }
        self._service.insert_entity(self._table_name, task)

    def remove_blog(self, email: str, title: str):
        self._service.delete_entity(self._table_name, email, title)

    def get_blog(self, email: str, title: str):
        try:
            return self._service.get_entity(self._table_name, email, title)
        except AzureMissingResourceHttpError:
            return None

    def add_tag(self, email: str, title: str, tag: str):
        entity = self._service.get_entity(self._table_name, email, title)
        tags_json = entity.get('Tags', '[]')
        tags: Set[str] = set(json.loads(tags_json))
        tags.add(tag)

        task = {
            'PartitionKey': email,
            'RowKey': title,
            'Tags': json.dumps(list(tags)),
            'LastModifiedUtc': datetime.utcnow().isoformat()
        }
        self._service.merge_entity(self._table_name, task)

    def remove_tag(self, email: str, title: str, tag: str):
        entity = self._service.get_entity(self._table_name, email, title)
        tags_json = entity.get('Tags', '[]')
        tags: Set[str] = set(json.loads(tags_json))
        tags.remove(tag)

        task = {
            'PartitionKey': email,
            'RowKey': title,
            'Tags': json.dumps(list(tags)),
            'LastModifiedUtc': datetime.utcnow().isoformat()
        }
        self._service.merge_entity(self._table_name, task)
