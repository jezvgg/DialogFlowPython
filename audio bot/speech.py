import speech_recognition as s_r
from gtts import gTTS
import soundfile as sf
from pathlib import Path
import os


def STT(audio_path: str) -> str:
    '''
    Speech-to-Text function.
    Taking path to audio file (.oga format)
    Return text of audio file.
    '''
    # Reading and exporting to WAV
    data, sample = sf.read(audio_path)
    sf.write('audio.wav', data, sample)
    print('Audio exported to WAV')

    # Creating recognaizer and special audiofile for lib
    recognaizer = s_r.Recognizer()
    audio_file = s_r.AudioFile('audio.wav')

    # Cleaning audio file
    with audio_file as source:
        recognaizer.adjust_for_ambient_noise(source)
        recorded_audio = recognaizer.listen(source)
    print('Audio cleaned')

    # Recognizing audio file
    alt = recognaizer.recognize_google(
        recorded_audio,
        language='ru-RU',
        show_all=True
     )
    try:
        text = alt['alternative'][0]['transcript']
    except TypeError:
        print('typeError')
        text = 'Не получилось разобрать аудиосообщение, отправитье пожалуйста ещё раз. Желательно с задержкой в начале.'
    
    os.remove(audio_path)
    os.remove('audio.wav')
    return text


def TTS(text: str):
    '''
    Take text that need to convert to audio.
    Return path to audio file. (mp3 format)
    '''
    obj = gTTS(text = text, lang='ru', slow=False)
    obj.save('output.mp3')
    return Path(os.getcwd(), 'output.mp3')