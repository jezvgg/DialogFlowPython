import json
from google.cloud import dialogflow


class settings:
    '''
    Класс настроек.
    '''
    __settings = None
    bot_token = ''
    client_secret = ''
    __session_client = None
    __session = None
    project_id = ''
    session_id = ''
    language = ''
    counter = 0
    last_params = 0

    def __init__(self, settings_url):

        settings_file = open(settings_url)
        self.__settings = json.load(settings_file) # Открытие json файла с настройками

        self.bot_token = self.__settings['bot-token'] # Токен телеграмм бота

        self.__client_secret = self.__settings['client-secret'] # json файл для работы с Google Sheets
        
        self.project_id = self.__settings['project_id'] # ID проекта
        self.session_id = self.__settings['session_id']
        self.language = self.__settings['language']

        self.__session_client = dialogflow.SessionsClient() # Создание сессии для DialogFlow
        self.__session = self.__session_client.session_path(self.project_id, self.session_id)

    def sheets(self):
        '''
        Возращает класс sheets для работы с Google Таблицами.
        '''
        return self.__sheets
    
    def session_client(self):
        '''
        Возращает session_client для работы с DialogFlow.
        '''
        return self.__session_client
    
    def session(self):
        '''
        Возращает session для работы с DialogFlow.
        '''
        return self.__session