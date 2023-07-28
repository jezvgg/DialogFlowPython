from google.cloud import dialogflow
import json
from pathlib import Path

# upload file with settings
settings_file = open(Path('settings.json'))
settings = json.load(settings_file)


test_text = input()

# create session to work with DialogFlow
session_client = dialogflow.SessionsClient()
session = session_client.session_path(settings['project_id'], settings['session_id'])

# create special text class for dialogflow and send query to dialogflow
text_input = dialogflow.TextInput(text=test_text, language_code="RU")
query_input = dialogflow.QueryInput(text=text_input)

# take response from dialogflow
response = session_client.detect_intent(
    request={"session": session, "query_input": query_input}
    )

print("Query text: {}".format(response.query_result.query_text))
print(
    "Intent detected: {}".format(
        response.query_result.intent.display_name
    )
 )
print("Returned text: {}\n".format(response.query_result.fulfillment_text))
