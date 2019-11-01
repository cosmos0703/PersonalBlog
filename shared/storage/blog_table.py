from typing import Set, List, Dict
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

    def get_blog(self, email: str, title: str) -> Dict[str, str]:
        try:
            return self._service.get_entity(self._table_name, email, title)
        except AzureMissingResourceHttpError:
            return None

    def list_blogs(self) -> List[Dict[str, str]]:
        return self._list_blogs(100)

    def list_blogs_by_author(self, email: str) -> List[Dict[str, str]]:
        return self._list_blogs_by_author(email)

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

    def _list_blogs(self, limit: int):
        result: List[str] = []
        entities = self._service.query_entities(self._table_name)
        result.extend([e.get('Title') for e in entities])
        return result

    def _list_blogs_by_author(self, email: str):
        result: List[str] = []
        entities = self._service.query_entities(self._table_name, f"PartitionKey eq '{email}'")
        result.extend([e.get('Title') for e in entities])
        return result
