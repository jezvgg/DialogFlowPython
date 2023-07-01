from google.cloud import dialogflow
from settings import settings

def response(settings: settings, text: str) -> dialogflow.SessionsClient.detect_intent: 
    '''
        Получает класс настроек, после чего из него получает ссесию и отправляет
        запрос к DialogFlow.
        text - текст, который будет в запросе к DialogFlow
        Вернёт результат запроса, из которого можно взять query_result.
    '''
    text_input = dialogflow.TextInput(text=text, language_code=settings.language) # Ввод текста
    query_input = dialogflow.QueryInput(text=text_input) # Запрос к агенту по тексту
    session_client = settings.session_client()
    session = settings.session()

    response = session_client.detect_intent(
    request={"session": session, "query_input": query_input}
    )

    return response