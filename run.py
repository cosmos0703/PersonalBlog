import os
from shared.storage import BlogTable, UserTable

def main():
    azureWebJobsStorage = os.getenv('AzureWebJobsStorage')
    if not azureWebJobsStorage:
        raise Exception("Environment variable AzureWebJobsStorage needs to be set")

    bt = BlogTable()
    if not bt.exist_table():
        bt.create_table()

    ut = UserTable()
    if not ut.exist_table():
        ut.create_table()

if __name__ == '__main__':
    main()
