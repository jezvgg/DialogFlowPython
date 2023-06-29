from google.cloud import dialogflow

def response(settings, text):
    text_input = dialogflow.TextInput(text=text, language_code=settings.language) # Ввод текста
    query_input = dialogflow.QueryInput(text=text_input) # Запрос к агенту по тексту
    session_client = settings.session_client()
    session = settings.session()

    response = session_client.detect_intent(
    request={"session": session, "query_input": query_input}
    )

    return response