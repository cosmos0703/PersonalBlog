import os

class BaseStorage:
    def __init__(self):
        self._connection_string = os.getenv('AzureWebJobsStorage')
