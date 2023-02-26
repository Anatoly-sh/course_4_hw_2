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
load_dotenv()


class Channel:
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
        service = build('youtube', 'v3', developerKey=os.getenv('SKYPROAPIKEY'))
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


"""    def save_json_in_file(self, path):
        метод сохраняет все атрибуты объекта channel, кроме json в файл по адресу path
        text = "["
        for dic in self.__dict__:
            if dic != 'json':
                text +=  "{'" + str(dic) + "':'" +str(self.__dict__[dic]) + "'}, \n"
        json_text = text[:-3] + "]"
        with open(path, "w", encoding="UTF-8") as file:
            file.write(str(json_text))"""


"""def __repr__(self):
        метод возвращает представление объекта channel
        text = ""
        for dic in self.__dict__:
            text += dic + "=" + str(self.__dict__[dic]) + ", "
        return text[:-2]"""


item = Channel(channel_id, "SKYPROAPIKEY")

item.print_info()

vdud = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA', "SKYPROAPIKEY")

# получаем значения атрибутов
print(vdud.title)
# вДудь
print(vdud.video_count)
# 163
print(vdud.url)
# https://www.youtube.com/channel/UCMCgOm8GZkHp8zJ6l7_hIuA

# менять не можем
# vdud.channel_id = 'Новое название'
# AttributeError: property 'channel_id' of 'Channel' object has no setter

# можем получить объект для работы с API вне класса
print(Channel.get_service())
# <googleapiclient.discovery.Resource object at 0x000002B1E54F9750>