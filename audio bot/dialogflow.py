from google.cloud import dialogflow
from pathlib import Path
import json

class DialogFlowHelper:
    language = ''
    session = None
    session_client = None

    def __init__(self, settings: str):
        '''
        class that help to work with DialogFlow.
        settings - path to your settings file (json format)
        '''
        settings_file = open(Path(settings))
        settings = json.load(settings_file)

        # create session to work with DialogFlow
        self.session_client = dialogflow.SessionsClient()                
        self.session = self.session_client.session_path(project=settings['project-id'], session=settings['session-id'])

        # language of user (might be ru-RU, en-US e.t.c)
        self.language = settings['language']

    def response(self, text: str):
        '''
        Take text that you want to ask your dialogflow agent.
        return answer of agent.
        Same that simple example
        '''
        # generete specified class text for dialogflow and query to dialogflow
        text_input = dialogflow.TextInput(text=text, language_code=self.language)
        query_input = dialogflow.QueryInput(text=text_input)

        # take response from dialogflow
        response = self.session_client.detect_intent(
        request={"session": self.session, "query_input": query_input}
        )
        return response
    
    def response_for_text(self, text:str) -> str:
        '''
        Take text that you want to ask your dialogflow agent.
        return answer of agent. (only text)
        Same that simple example
        '''
        return self.response(text=text).query_result.fulfillment_text