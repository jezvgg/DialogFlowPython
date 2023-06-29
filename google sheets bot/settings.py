import json
from google.cloud import dialogflow

class settings:
    __settings = None
    bot_token = ''
    client_secret = ''
    __session_client = None
    __session = None
    project_id = ''
    session_id = ''
    language = ''

    def __init__(self, settings_url):

        settings_file = open(settings_url)
        self.__settings = json.load(settings_file)

        self.bot_token = self.__settings['bot-token']

        self.__client_secret = self.__settings['client-secret']
        
        self.project_id = self.__settings['project_id']
        self.session_id = self.__settings['session_id']
        self.language = self.__settings['language']

        self.__session_client = dialogflow.SessionsClient()
        self.__session = self.__session_client.session_path(self.project_id, self.session_id)

    def sheets(self):
        return self.__sheets
    
    def session_client(self):
        return self.__session_client
    
    def session(self):
        return self.__session