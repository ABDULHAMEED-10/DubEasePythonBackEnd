from moviepy.video.io.VideoFileClip import VideoFileClip
import speech_recognition as sr
from googletrans import Translator
import os
from moviepy.editor import *
import subprocess




def extract_audio(video_path, audio_output_path):
    video_clip = VideoFileClip(video_path)
    os.makedirs(os.path.dirname(audio_output_path), exist_ok=True)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(audio_output_path)
    video_clip.close()
    return audio_output_path

def convert_audio_to_text(audio_path):
    
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        try:
            audio_data = recognizer.record(source, duration=1000)
            audio_text = recognizer.recognize_google(audio_data,language="ur-PK")
        except sr.UnknownValueError:
            raise Exception("Audio is inaudible. Please choose a different video.")
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
def convert_video_to_mp4(video_path):
    output_path = video_path.replace('.webm', '.mp4')
    subprocess.run(['ffmpeg', '-i', video_path, output_path])
    return output_path
def process_Ur_video(filename):
    video_output_path=""
    video_path = os.path.join('E:/DubEase/Python Server/uploads/', filename)
    audioFileExtension = 'audio.wav'
    pathOfAudioFile = 'output/audio/UrIn/'
    
    wordsToremove=['.mp4','.webm']
    for word in wordsToremove:
        filename = filename.replace(word,'')
    audio_output_path = f'{pathOfAudioFile}{filename}{audioFileExtension}'
   
    pathOfTextFile = 'output/text/UrIn/'
    textFileExtension = '.txt'
    text_output_path = f'{pathOfTextFile}{filename}{textFileExtension}'

    
    if video_path.lower().endswith(('.mp4')): 
        audio_output_path = extract_audio(video_path, audio_output_path)
    
    elif video_path.lower().endswith(('.webm')):
        video_output_path = convert_video_to_mp4(video_path)
        audio_output_path = extract_audio(video_output_path, audio_output_path)



    audio_text = convert_audio_to_text(audio_output_path)
    
    # Translate the text
    translated_text = translate_text(audio_text)
    # Save translated text to a file
    save_text_to_file(translated_text, text_output_path)
    print(video_output_path)
    return audio_output_path , translated_text , video_output_path
