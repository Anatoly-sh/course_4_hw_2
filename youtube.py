import os
import json
from googleapiclient.discovery import build

"""
Файл .env в корне проекта  — это текстовый файл, содержащий пары “ключ/значение” 
всех переменных среды. Необходимо установить библиотеку python-dotenv. load_dotenv() 
— для поиска файла .env и загрузки из него переменных среды.
"""
from dotenv import load_dotenv

channel_id = 'UCMCgOm8GZkHp8zJ6l7_hIuA'  # вДудь
load_dotenv()


class Channel:
    def __init__(self, channel_id):
        self.__id_channel = channel_id
        self.channel_info = self.get_service().channels().list(id=channel_id, part='snippet, statistics').execute()
        self.title = self.channel_info['items'][0]['snippet']['title']
        self.description = self.channel_info['items'][0]['snippet']['description']
        self.subscribers = self.channel_info['items'][0]['statistics']['subscriberCount']
        self.url = 'https://www.youtube.com/' + self.__id_channel
        self.subscriber_count = self.channel_info['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel_info['items'][0]['statistics']['videoCount']
        self.view_count = self.channel_info['items'][0]['statistics']['viewCount']

    def __str__(self):
        '''Метод возврата названия канала'''
        return f'Channel: {self.title}'

    @property
    def channel_id(self):
        return self.__id_channel

    @classmethod
    def get_service(cls):
        """метод класса, который возвращает объект для работы с API ютуба"""
        api_key: str = os.getenv('SKYPROAPIKEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def save_to_file(self, file_name):
        """запись статистики в файл"""
        with open(file_name, 'w', encoding='UTF-8') as file:
            json.dump(self.channel_info, file, indent=4, ensure_ascii=False)

    def print_info(self):
        """Статистика канала
        см. методы build() , channels() , list() , execute()"""
        self.info = json.dumps(self.channel_info, indent=4)
        return self.info

    def __add__(self, other):
        '''Метод сложения количества подписчиков'''
        return int(self.subscribers) + int(other.subscribers)

    def __gt__(self, other):
        '''Метод сравнения количества подписчиков >'''
        return int(self.subscribers) > int(other.subscribers)

    def __lt__(self, other):
        '''Метод сравнения количества подписчиков <'''
        return int(self.subscribers) < int(other.subscribers)


if __name__ == '__main__':
    ch1 = Channel('UC1eFXmJNkjITxPFWTy6RsWg')
    ch2 = Channel(channel_id)
    print(ch1)
    print(ch2)
    print(ch1 + ch2)
    print(ch1 > ch2)
    print(ch1 < ch2)




