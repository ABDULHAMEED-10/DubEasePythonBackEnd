import speech_recognition as sr
from googletrans import Translator
from pydub import AudioSegment
import os
import subprocess

def convert_audio_to_text(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        try:
            audio_data = recognizer.record(source, duration=1000)
            audio_text = recognizer.recognize_google(audio_data,language="ur-PK")
        except sr.UnknownValueError:
            raise Exception("Audio is inaudible. Please choose a different audio.")
        except sr.RequestError as e:
            raise Exception(f"Could not request results from Google Speech Recognition service; {e}")
        
    return audio_text

def translate_text(text, target_language='en'):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

def save_text_to_file(text, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(text)
def convert_audio_to_wav(audio_path, output_path):
    
    audio = AudioSegment.from_file(audio_path)
    output_path = audio_path.replace('.webm', '.wav')
    audio.export(output_path, format="wav")
    return output_path
    
def process_Ur_audio(filename):

    audio_path = os.path.join('E:/DubEase/Python Server/uploads/', filename)
    audio_output_path = 'output/audio/UrIn/'

    pathOfTextFile = 'output/text/UrIn/'
    textFileExtension = '.txt'
    text_output_path = f'{pathOfTextFile}{filename}{textFileExtension}'

   
    try:
        
        if audio_path.lower().endswith('.wav'):
            
            audio_output_path = audio_path
        elif audio_path.lower().endswith(('.mp3', '.mpeg', '.ogg','.webm')):
            audio_output_path = convert_audio_to_wav(audio_path, audio_output_path)
            
     
        audio_text = convert_audio_to_text(audio_output_path)
       
        translated_text = translate_text(audio_text)

        save_text_to_file(translated_text, text_output_path)
        return audio_output_path , translated_text
    except Exception as e:
        print(f"Error occurred during processing: {e}")





