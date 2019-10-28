from typing import Dict, Set, List
import os
import json
from datetime import datetime
from azure.common import AzureMissingResourceHttpError
from .base_table import BaseTable

class UserBlogsTable(BaseTable):
    DefaultTableName = 'PristineUserBlogsTable'
    DefaultPartitionKey = 'UserBlogsTable'

    def __init__(self, table_name: str = None):
        super().__init__(table_name or UserBlogsTable.DefaultTableName)

    def add_blog_to_user(self, email: str, title: str):
        entity = self._get_or_create_blog(email)
        self._add_blog_to_entity(entity, title)
        self._update_last_modified_time(entity)
        self._service.insert_or_merge_entity(self._table_name, entity)

    def remove_blog_from_user(self, email: str, title: str):
        entity = self._get_or_create_blog(email)
        self._remove_blog_from_entity(entity, title)
        self._update_last_modified_time(entity)
        self._service.insert_or_merge_entity(self._table_name, entity)

    def list_blogs_from_user(self, email: str) -> List[str]:
        return self._list_blogs(email)

    def _get_or_create_blog(self, email: str):
        try:
            entity = self._service.get_entity(
                self._table_name, UserBlogsTable.DefaultPartitionKey, email)
        except AzureMissingResourceHttpError:
            entity = self._create_blog_user_relationship(email)
        return entity

    def _list_blogs(self, email: str) -> List[str]:
        try:
            entity = self._service.get_entity(
                self._table_name, UserBlogsTable.DefaultPartitionKey, email)
        except AzureMissingResourceHttpError:
            return []
        return json.loads(entity.get('Blogs', '[]'))

    def _create_blog_user_relationship(self, email: str):
        return {
            'PartitionKey': UserBlogsTable.DefaultPartitionKey,
            'RowKey': email,
            'Author': email,
            'Blogs': '[]',
            'CreatedUtc': datetime.utcnow().isoformat(),
            'LastModifiedTime': None
        }

    def _add_blog_to_entity(self, entity: Dict[str, str], blog: str):
        blogs: Set[str] = set(json.loads(entity.get('Blogs', '[]')))
        blogs.add(blog)
        entity['Blogs'] = json.dumps(list(blogs))

    def _remove_blog_from_entity(self, entity: Dict[str, str], blog: str):
        blogs: Set[str] = set(json.loads(entity.get('Blogs', '[]')))
        blogs.remove(blog)
        entity['Blogs'] = json.dumps(list(blogs))

    def _update_last_modified_time(self, entity: Dict[str, str]):
        entity['LastModifiedTime'] = datetime.utcnow().isoformat()
