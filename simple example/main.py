from google.cloud import dialogflow # библеотека для работы с DialogFlow
import json
from pathlib import Path # Создание пути для всех ОС


settings_file = open(Path('settings.json')) # Загружаем json файл с настройками
settings = json.load(settings_file)

project_id = settings['project_id'] # Записываем настройки
session_id = settings['session_id']
language = settings['language']
test_text = 'Привет'


session_client = dialogflow.SessionsClient()                # Создание сессии
session = session_client.session_path(project_id, session_id)


text_input = dialogflow.TextInput(text=test_text, language_code=language) # Ввод текста
query_input = dialogflow.QueryInput(text=text_input) # Запрос к агенту по тексту

# Кидаем запрос
response = session_client.detect_intent(
    request={"session": session, "query_input": query_input}
    )

# Результат
print("Текст запроса: {}".format(response.query_result.query_text))
print(
    "Обрабатывающий интент: {}".format(
        response.query_result.intent.display_name
    )
 )
print("Текст ответа: {}\n".format(response.query_result.fulfillment_text))
