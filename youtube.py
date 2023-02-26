import os
import json
from googleapiclient.discovery import build

"""
Файл .env в корне проекта  — это текстовый файл, содержащий пары “ключ/значение” 
всех переменных среды. Необходимо установить библиотеку python-dotenv. load_dotenv() 
— для поиска файла .env и загрузки из него переменных среды.
"""
from dotenv import load_dotenv

# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
# api_key: str = os.getenv('SKYPROAPIKEY')

# создать специальный объект для работы с API
# youtube = build('youtube', 'v3', developerKey=api_key)

channel_id = 'UCMCgOm8GZkHp8zJ6l7_hIuA'  # вДудь


# channel_id = 'UC1eFXmJNkjITxPFWTy6RsWg'       # Редакция
# channel_id = 'UClMe70teNK5LpBE3Im_JRSQ'  # Знай ТВ

# channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()

# print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))
class YoutubeAnalytic:
    load_dotenv()

    def __init__(self, id_channel, api_key):
        self.api_key = os.getenv(api_key)  # ключ из .env
        self.__id_channel = id_channel
        # специальный объект для работы с API
        self.service = build('youtube', 'v3', developerKey=self.api_key)
        self.channel_info = self.service.channels().list(id=channel_id, part='snippet,statistics').execute()

        self.title = self.channel_info['items'][0]['snippet']['title']
        self.description = self.channel_info['items'][0]['snippet']['description']
        self.url = 'https://www.youtube.com/' + self.__id_channel
        self.subscriber_count = self.channel_info['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel_info['items'][0]['statistics']['videoCount']
        self.view_count = self.channel_info['items'][0]['statistics']['viewCount']
        data = self.title + self.description + self.url + self.subscriber_count + self.video_count + self.view_count

    @classmethod
    def get_service(cls):
        service = build('youtube', 'v3', developerKey=os.environ.get('YOUTUBE_KEY'))
        return service

    def json_file(self, data, filename='channel.json'):
        """добавляет в json файл информацию о канале, хранящуюся в атрибутах"""
        with open(filename, 'r') as file:
            file_data = json.load(file)
            file_data.append(data)
            return json.dump(file_data, file, indent=4)

    def print_info(self):
        # см. методы build() , channels() , list() , execute()
        print(json.dumps(self.channel_info, indent=2, ensure_ascii=False))


item = YoutubeAnalytic(channel_id, "SKYPROAPIKEY")

item.print_info()
