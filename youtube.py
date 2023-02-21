import os
import json
from googleapiclient.discovery import build
import pprint
"""
Файл .env в корне проекта  — это текстовый файл, содержащий пары “ключ/значение” 
всех переменных среды. Необходимо установить библиотеку python-dotenv. load_dotenv() 
— для поиска файла .env и загрузки из него переменных среды.
"""
from dotenv import load_dotenv

load_dotenv()

# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
# api_key: str = os.getenv('SKYPROAPIKEY')

# создать специальный объект для работы с API
# youtube = build('youtube', 'v3', developerKey=api_key)

# channel_id = 'UCMCgOm8GZkHp8zJ6l7_hIuA'       # вДудь
# channel_id = 'UC1eFXmJNkjITxPFWTy6RsWg'       # Редакция
channel_id = 'UClMe70teNK5LpBE3Im_JRSQ'         # Знай ТВ

# channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()

# print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))
class Youtube_analitica:

    def __init__(self, id_channel, api_key):
        self.api_key = os.getenv(api_key)                       # ключ из .env
        self.id_channel = id_channel
        # специальный объект для работы с API
        self.service = build('youtube', 'v3', developerKey=self.api_key)

    def print_info(self):
        # см. методы build() , channels() , list() , execute()
        self.info = json.dumps(self.service.channels().list(id=self.id_channel, part='snippet,statistics').execute())
        return self.info


item = Youtube_analitica(channel_id, "SKYPROAPIKEY")

# print(item.print_info())

pprint.pprint(item.print_info())
