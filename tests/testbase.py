import os
import unittest
import json
from shared import config

class Testbase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._root = config.ROOT_DIR
        cls._local_json_path = os.path.join(config.ROOT_DIR, 'local.settings.json')

        with open(cls._local_json_path) as j:
            json_dict = json.load(j)
            cls._azure_webjobs_storage = json_dict['Values']['AzureWebJobsStorage']

        if cls._azure_webjobs_storage is None:
            cls._azure_webjobs_storage = os.getenv('AzureWebJobsStorage')

        if cls._azure_webjobs_storage is None:
            raise Exception("AzureWebJobsStorage is not found")

        os.environ['AzureWebJobsStorage'] = cls._azure_webjobs_storage
