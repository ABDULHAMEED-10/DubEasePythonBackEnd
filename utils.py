import shutil
import speech_recognition as sr
from googletrans import Translator
from pydub import AudioSegment
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import *
import subprocess

def convert_audio_to_text(audio_path,sourcelanguage):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        try:
            audio_data = recognizer.record(source, duration=1000)
            audio_text = recognizer.recognize_google(audio_data, language=sourcelanguage)
        except sr.UnknownValueError:
            raise Exception("Audio is inaudible. Please choose a different audio.")
        except sr.RequestError as e:
            raise Exception(f"Could not request results from Google Speech Recognition service; {e}")
        
    return audio_text
def translate_text(text, target_language):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text
def save_text_to_file(text, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(text)

def convert_audio_to_wav(audio_path, output_path=None):
    audio = AudioSegment.from_file(audio_path)
    if not output_path:
        output_path = audio_path.replace('.webm', '.wav')
    audio.export(output_path, format="wav")
    return output_path

def extract_audio(video_path, audio_output_path):
    
    video_clip = VideoFileClip(video_path)
    
    os.makedirs(os.path.dirname(audio_output_path), exist_ok=True)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(audio_output_path)
    video_clip.close()
    return audio_output_path

def convert_video_to_mp4(video_path):
    
    output_path = video_path.replace('.webm', '.mp4')
    subprocess.run(['ffmpeg', '-i', video_path, output_path])
    return output_path


def delete_folder(file_paths):
    for file_path in file_paths:
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
        else:
            os.remove(file_path)
    return True

